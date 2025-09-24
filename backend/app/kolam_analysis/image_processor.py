import cv2
import numpy as np
from typing import List
from .models import Dot

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Converts a color image to a clean, binary format suitable for line analysis."""
    if image is None: 
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Adaptive thresholding is excellent for handling variations in lighting.
    # THRESH_BINARY_INV makes the kolam lines white (255) and the background black (0).
    binary_image = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    return binary_image

def detect_dots(image: np.ndarray) -> List[Dot]:
    """Detects black, circular dots (pulli) using multiple detection methods for robustness."""
    if image is None or image.size == 0:
        return []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Method 1: Hough Circle Transform for circular dots
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
        param1=50, param2=30, minRadius=3, maxRadius=15
    )

    dots = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center_x, center_y, radius = circle
            # Check if the center is dark (dot) and surroundings are light (background)
            center_intensity = gray[center_y, center_x]
            if center_intensity < 100:  # Dark center
                dots.append(Dot(x=int(center_x), y=int(center_y), radius=int(radius)))

    # Method 2: Contour-based detection for irregular dots
    if len(dots) < 5:  # If Hough didn't find enough, try contours
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if 20 < area < 1000:  # Reasonable dot size
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > 0.5:  # Somewhat circular
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            center_x = int(M["m10"] / M["m00"])
                            center_y = int(M["m01"] / M["m00"])
                            # Avoid duplicates
                            if not any(abs(dot.x - center_x) < 10 and abs(dot.y - center_y) < 10 for dot in dots):
                                dots.append(Dot(x=center_x, y=center_y, radius=5))

    # Method 3: SimpleBlobDetector as fallback with relaxed parameters
    if len(dots) < 3:
        inverted_gray = 255 - gray

        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByArea = True
        params.minArea = 5  # More relaxed
        params.maxArea = 1000
        params.filterByCircularity = True
        params.minCircularity = 0.3  # More relaxed
        params.filterByConvexity = True
        params.minConvexity = 0.5  # More relaxed
        params.filterByInertia = True
        params.minInertiaRatio = 0.1  # More relaxed

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(inverted_gray)

        for kp in keypoints:
            center_x, center_y = int(kp.pt[0]), int(kp.pt[1])
            # Avoid duplicates
            if not any(abs(dot.x - center_x) < 10 and abs(dot.y - center_y) < 10 for dot in dots):
                dots.append(Dot(x=center_x, y=center_y, radius=int(kp.size / 2)))

    return dots