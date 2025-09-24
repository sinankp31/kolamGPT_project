import cv2
import numpy as np
from typing import List, Tuple
from .models import Dot
from scipy import ndimage

# Optional imports with fallbacks
try:
    from skimage import morphology, filters
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False

try:
    from sklearn.cluster import DBSCAN
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def advanced_preprocess_image(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Advanced multi-stage image preprocessing for optimal kolam analysis.

    Returns:
        Tuple of (binary_image, enhanced_gray, edge_map)
    """
    if image is None or image.size == 0:
        return None, None, None

    # Stage 1: Color space conversion with gamma correction
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply gamma correction for better contrast
    gamma = 1.2
    gamma_corrected = np.power(gray / 255.0, gamma) * 255.0
    gamma_corrected = gamma_corrected.astype(np.uint8)

    # Stage 2: Multi-scale Gaussian blur for noise reduction
    blurred_multi = cv2.GaussianBlur(gamma_corrected, (3, 3), 0)
    blurred_multi = cv2.addWeighted(blurred_multi, 1.5, gamma_corrected, -0.5, 0)

    # Stage 3: CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(blurred_multi)

    # Stage 4: Advanced thresholding with multiple techniques
    # Adaptive Gaussian thresholding
    binary_adaptive = cv2.adaptiveThreshold(
        enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 15, 3
    )

    # Otsu's thresholding on blurred image
    _, binary_otsu = cv2.threshold(enhanced_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Combine thresholding results
    binary_combined = cv2.bitwise_or(binary_adaptive, binary_otsu)

    # Stage 5: Morphological operations for cleaning
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    binary_cleaned = cv2.morphologyEx(binary_combined, cv2.MORPH_OPEN, kernel, iterations=1)
    binary_cleaned = cv2.morphologyEx(binary_cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Stage 6: Edge detection for line analysis
    edges = cv2.Canny(enhanced_gray, 50, 150, apertureSize=3)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    return binary_cleaned, enhanced_gray, edges_dilated

def detect_dots_advanced(image: np.ndarray) -> List[Dot]:
    """
    State-of-the-art dot detection using multiple advanced computer vision techniques.
    """
    if image is None or image.size == 0:
        return []

    # Get advanced preprocessing results
    binary_image, enhanced_gray, edge_map = advanced_preprocess_image(image)

    if binary_image is None:
        return []

    all_dots = []

    # Method 1: Enhanced Hough Circle Transform with optimized parameters
    circles = cv2.HoughCircles(
        enhanced_gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=15,
        param1=40, param2=25, minRadius=2, maxRadius=20
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center_x, center_y, radius = circle

            # Advanced validation: check local region properties
            if _validate_dot_region(enhanced_gray, center_x, center_y, radius):
                dot = Dot(x=int(center_x), y=int(center_y), radius=int(radius))
                all_dots.append(dot)

    # Method 2: Contour analysis with advanced shape filtering
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if 10 < area < 2000:  # Expanded range for various dot sizes
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                # Multiple shape descriptors
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                compactness = (perimeter * perimeter) / (4 * np.pi * area)

                # Bounding box analysis
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = min(w, h) / max(w, h) if max(w, h) > 0 else 0

                # Advanced filtering
                if (circularity > 0.4 and compactness < 2.0 and
                    aspect_ratio > 0.6 and w > 3 and h > 3):

                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        center_x = int(M["m10"] / M["m00"])
                        center_y = int(M["m01"] / M["m00"])

                        # Avoid duplicates with improved distance check
                        if not _is_duplicate_dot(all_dots, center_x, center_y, min(w, h) // 2):
                            radius = min(w, h) // 2
                            all_dots.append(Dot(x=center_x, y=center_y, radius=radius))

    # Method 3: Advanced blob detection with machine learning-like features
    if len(all_dots) < 5:
        inverted_gray = 255 - enhanced_gray

        # Multi-scale blob detection
        for scale in [1.0, 1.2, 0.8]:
            params = cv2.SimpleBlobDetector_Params()

            # Optimized parameters for kolam dots
            params.filterByColor = True
            params.blobColor = 255
            params.filterByArea = True
            params.minArea = int(8 * scale)
            params.maxArea = int(1500 * scale)
            params.filterByCircularity = True
            params.minCircularity = 0.35
            params.filterByConvexity = True
            params.minConvexity = 0.4
            params.filterByInertia = True
            params.minInertiaRatio = 0.05

            detector = cv2.SimpleBlobDetector_create(params)
            keypoints = detector.detect(inverted_gray)

            for kp in keypoints:
                center_x, center_y = int(kp.pt[0]), int(kp.pt[1])
                radius = int(kp.size / 2 * scale)

                if not _is_duplicate_dot(all_dots, center_x, center_y, radius):
                    all_dots.append(Dot(x=center_x, y=center_y, radius=radius))

    # Method 4: Template matching for known dot patterns (advanced)
    if len(all_dots) < 3:
        all_dots.extend(_template_based_detection(enhanced_gray))

    # Method 5: Clustering-based detection for dense patterns
    if len(all_dots) > 10:
        all_dots = _cluster_and_filter_dots(all_dots)

    # Final validation and ranking
    validated_dots = []
    for dot in all_dots:
        if _validate_dot_comprehensive(image, enhanced_gray, dot):
            validated_dots.append(dot)

    return validated_dots[:200]  # Limit for performance

def _validate_dot_region(gray_image: np.ndarray, x: int, y: int, radius: int) -> bool:
    """Advanced validation of dot regions using local statistics."""
    height, width = gray_image.shape

    # Ensure coordinates are within bounds
    if not (radius <= x < width - radius and radius <= y < height - radius):
        return False

    # Extract local region
    region = gray_image[y-radius:y+radius+1, x-radius:x+radius+1]

    if region.size == 0:
        return False

    # Statistical analysis
    center_intensity = gray_image[y, x]
    region_mean = np.mean(region)
    region_std = np.std(region)

    # Advanced criteria
    is_dark_center = center_intensity < region_mean - region_std
    has_contrast = region_std > 15
    reasonable_size = 2 <= radius <= 25

    return is_dark_center and has_contrast and reasonable_size

def _is_duplicate_dot(dots: List[Dot], x: int, y: int, radius: int, threshold: int = 12) -> bool:
    """Improved duplicate detection with adaptive thresholds."""
    for dot in dots:
        distance = np.sqrt((dot.x - x) ** 2 + (dot.y - y) ** 2)
        size_diff = abs(dot.radius - radius)
        adaptive_threshold = max(threshold, (dot.radius + radius) * 0.3)

        if distance < adaptive_threshold and size_diff < radius * 0.5:
            return True
    return False

def _template_based_detection(gray_image: np.ndarray) -> List[Dot]:
    """Template matching for known kolam dot patterns."""
    dots = []

    # Create dot templates of various sizes
    template_sizes = [5, 7, 10, 12, 15]
    templates = []

    for size in template_sizes:
        template = np.zeros((size*2+1, size*2+1), dtype=np.uint8)
        cv2.circle(template, (size, size), size, 255, -1)
        templates.append((template, size))

    # Apply template matching
    for template, radius in templates:
        result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6

        locations = np.where(result >= threshold)
        for pt in zip(*locations[::-1]):
            x, y = pt[0] + radius, pt[1] + radius

            if not _is_duplicate_dot(dots, x, y, radius):
                dots.append(Dot(x=x, y=y, radius=radius))

    return dots

def _cluster_and_filter_dots(dots: List[Dot]) -> List[Dot]:
    """Use clustering to identify and filter dot groups."""
    if len(dots) < 3 or not SKLEARN_AVAILABLE:
        return dots

    try:
        # Prepare data for clustering
        positions = np.array([[dot.x, dot.y] for dot in dots])

        # DBSCAN clustering to identify dot groups
        clustering = DBSCAN(eps=30, min_samples=2).fit(positions)
        labels = clustering.labels_

        filtered_dots = []
        for i, dot in enumerate(dots):
            if labels[i] != -1:  # Not noise
                cluster_dots = [d for j, d in enumerate(dots) if labels[j] == labels[i]]
                # Keep the most representative dot from each cluster
                if dot == _select_best_dot_from_cluster(cluster_dots):
                    filtered_dots.append(dot)

        return filtered_dots if filtered_dots else dots
    except Exception:
        # Fallback to original dots if clustering fails
        return dots

def _select_best_dot_from_cluster(cluster_dots: List[Dot]) -> Dot:
    """Select the best dot from a cluster based on multiple criteria."""
    if len(cluster_dots) == 1:
        return cluster_dots[0]

    # Score each dot based on multiple factors
    scores = []
    for dot in cluster_dots:
        # Prefer more circular dots, appropriate size, central position
        size_score = 1.0 if 4 <= dot.radius <= 15 else 0.5
        position_score = 1.0  # Could be enhanced with pattern analysis
        score = size_score * position_score
        scores.append(score)

    best_idx = np.argmax(scores)
    return cluster_dots[best_idx]

def _validate_dot_comprehensive(original_image: np.ndarray, gray_image: np.ndarray, dot: Dot) -> bool:
    """Comprehensive dot validation using multiple criteria."""
    height, width = original_image.shape[:2]

    # Boundary check
    if not (dot.radius <= dot.x < width - dot.radius and
            dot.radius <= dot.y < height - dot.radius):
        return False

    # Color analysis (ensure it's dark on light background)
    center_color = original_image[dot.y, dot.x]
    if len(original_image.shape) == 3:  # BGR image
        brightness = float(np.mean(center_color))
    else:  # Grayscale
        brightness = float(center_color)

    # Should be darker than surroundings
    region = gray_image[max(0, dot.y-5):min(height, dot.y+6),
                       max(0, dot.x-5):min(width, dot.x+6)]
    if region.size > 0:
        region_mean = float(np.mean(region))
        if brightness >= region_mean:
            return False

    # Size validation
    if not (2 <= dot.radius <= 25):
        return False

    # Shape validation using contour analysis
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, (dot.x, dot.y), dot.radius, 255, -1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        area = cv2.contourArea(contours[0])
        expected_area = np.pi * dot.radius * dot.radius
        area_ratio = area / expected_area

        # Should be reasonably circular
        if not (0.5 <= area_ratio <= 1.5):
            return False

    return True

# Legacy function for backward compatibility
def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Legacy preprocessing function."""
    binary, _, _ = advanced_preprocess_image(image)
    return binary

def detect_dots(image: np.ndarray) -> List[Dot]:
    """Legacy dot detection function - now uses advanced methods."""
    return detect_dots_advanced(image)