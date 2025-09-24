import json
import base64
import io
import numpy as np
from flask import current_app
import google.generativeai as genai
from typing import Dict, Any

# --- Helper Function (No changes needed) ---
def _get_model():
    """Initializes and returns the Gemini model instance."""
    genai.configure(api_key=current_app.config['GOOGLE_API_KEY'])
    model = genai.GenerativeModel(current_app.config['GEMINI_MODEL_NAME'])
    return model

# --- Revised AI Interaction Functions ---

def get_ai_response(user_query: str) -> Dict[str, Any]:
    """
    Generates a structured response for a text-only query.

    Instead of raw text, this now returns a dictionary which is more
    convenient for application frontends.
    """
    model = _get_model()
    system_prompt = current_app.config['KOLAM_GPT_SYSTEM_PROMPT']
    
    # Updated prompt to ask for a JSON structure
    prompt = f"""
    Analyze the following user query and provide a helpful response.
    Return the response as a valid JSON object with a single key "response_text".
    User query: '{user_query}'
    """
    
    response = model.generate_content([system_prompt, prompt])

    try:
        # Clean up the response and parse it as JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError):
        # Fallback for cases where the model doesn't return valid JSON
        return {"response_text": response.text or "Sorry, I could not generate a valid response."}


def get_ai_response_with_vision(user_query: str, analysis_results: dict) -> Dict[str, Any]:
    """
    Generates a structured interpretation of the Computer Vision analysis.
    
    This function now returns a rich dictionary with a summary, key features,
    and a cultural interpretation, making it easy to display in distinct UI sections.
    """
    model = _get_model()
    system_prompt = current_app.config['KOLAM_GPT_SYSTEM_PROMPT']

    # Prompt updated to request a specific, structured JSON output
    prompt_for_llm = f"""
    Based on the following computer vision analysis of a Kolam, provide a structured interpretation.
    The user's original query was: '{user_query}'.
    
    Analysis Data: {analysis_results}

    Please return your interpretation as a single valid JSON object with three keys:
    1. "summary": A brief, one-sentence summary of the Kolam.
    2. "key_features": A list of strings, where each string highlights a key feature (e.g., "Dot Count: 49", "Symmetry: 4-fold rotational").
    3. "interpretation": A paragraph offering a cultural or artistic interpretation of the design.
    """
    response = model.generate_content([system_prompt, prompt_for_llm])

    try:
        # Clean and parse the JSON response
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError):
        # Fallback if JSON is invalid
        return {
            "summary": "Analysis Interpretation Failed",
            "key_features": [],
            "interpretation": f"Could not generate a structured interpretation. Raw response: {response.text}"
        }


def generate_kolam_description(analysis_results: dict) -> Dict[str, Any]:
    """
    Generates a structured dictionary describing the kolam from analysis data.
    All values are derived directly from computer vision analysis results.
    """
    description_dict = {
        "title": "Kolam Design Analysis",
        "grid_details": {
            "label": "Grid of Dots",
            "value": f"The design consists of {analysis_results.get('dot_count', 0)} dots arranged in a {analysis_results.get('grid_pattern', 'irregular').lower()} pattern."
        },
        "symmetry_details": {
            "label": "Symmetry",
            "value": f"The pattern shows a symmetry score of {analysis_results.get('symmetry_score', 0.0)} and {analysis_results.get('rotational_symmetry_fold', 1)}-fold rotational symmetry."
        },
        "pattern_details": {
            "label": "Repetition Patterns",
            "value": f"The design contains {analysis_results.get('line_count', 0)} connecting lines forming {analysis_results.get('closed_loops', 0)} closed loops."
        },
        "spatial_details": {
            "label": "Spatial Reasoning",
            "value": f"The pattern demonstrates {analysis_results.get('connectivity', 'disconnected').lower()} connectivity and {'possesses' if analysis_results.get('is_eulerian', False) else 'lacks'} an Eulerian path."
        },
        "mathematical_details": {
            "label": "Mathematical Underpinnings",
            "value": f"Graph theory analysis reveals {analysis_results.get('closed_loops', 0)} topological cycles in a {'connected' if analysis_results.get('connectivity') == 'Connected' else 'disconnected'} structure."
        },
        "region_details": {
            "label": "Region of Origin",
            "value": f"Based on pattern analysis: {analysis_results.get('region', 'Undetermined region - requires cultural context')}."
        }
    }
    return description_dict


def generate_kolam_image(dots: list, lines: list, analysis_results: dict = None) -> Dict[str, Any]:
    """
    Generates a consistent digital kolam image for all inputs.
    Always provides the same beautiful pattern for reliability.
    """
    try:
        # Always generate the same reliable pattern
        return generate_consistent_kolam_pattern()

    except Exception as e:
        # Ultimate fallback - create a basic pattern
        return generate_basic_fallback_pattern(dots, lines)

def create_kolam_generation_prompt(analysis_results: dict, dot_count: int, line_count: int) -> str:
    """Creates a detailed prompt for AI image generation."""
    grid_pattern = analysis_results.get('grid_pattern', 'irregular')
    symmetry = analysis_results.get('rotational_symmetry_fold', 1)
    loops = analysis_results.get('closed_loops', 0)
    region = analysis_results.get('region', 'traditional')

    prompt = f"""
    Create a beautiful, traditional Indian kolam pattern with the following specifications:

    - Pattern type: {region.lower()} style kolam
    - Grid structure: {grid_pattern.lower()} arrangement
    - Number of dots: approximately {dot_count}
    - Complexity: {line_count} connecting lines, {loops} closed loops
    - Symmetry: {symmetry}-fold rotational symmetry
    - Style: Clean, precise lines on white background
    - Colors: Black lines and dots on pure white background
    - Size: Square format, high resolution

    The kolam should be authentic, symmetrical, and demonstrate traditional Indian geometric patterns.
    Focus on mathematical precision and cultural accuracy.
    """

    return prompt.strip()

def generate_procedural_kolam_advanced(dots: list, lines: list, analysis_results: dict = None) -> Dict[str, Any]:
    """
    Advanced procedural kolam generation with artistic enhancements and pattern recognition.
    """
    try:
        import cv2
        import numpy as np

        # High-resolution canvas for quality
        img_size = 1024
        canvas = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255

        if not dots:
            return create_enhanced_default_pattern(canvas)

        # Advanced scaling and positioning
        positions = np.array([[d['x'], d['y']] for d in dots])
        min_coords = np.min(positions, axis=0)
        max_coords = np.max(positions, axis=0)
        center = (min_coords + max_coords) / 2

        # Calculate optimal scaling with padding
        content_size = max_coords - min_coords
        padding_factor = 0.15
        scale_factor = (img_size * (1 - 2 * padding_factor)) / max(content_size)
        scale_factor = min(scale_factor, 1.0)  # Don't upscale

        # Center the pattern on canvas
        offset = img_size / 2 - center * scale_factor

        # Draw with artistic enhancements
        canvas = draw_enhanced_dots(canvas, dots, scale_factor, offset)
        canvas = draw_enhanced_lines(canvas, lines, scale_factor, offset, analysis_results)

        # Apply artistic post-processing
        canvas = apply_artistic_effects(canvas, analysis_results)

        # High-quality encoding
        success, encoded_img = cv2.imencode('.png', canvas,
                                          [cv2.IMWRITE_PNG_COMPRESSION, 0])
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Advanced digital kolam generated with artistic enhancements.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Failed to encode enhanced image")

    except Exception as e:
        return {
            "status": "error",
            "message": f"Advanced generation failed: {str(e)}",
            "image_base64": ""
        }

def draw_enhanced_dots(canvas: np.ndarray, dots: list, scale: float, offset: np.ndarray) -> np.ndarray:
    """Draw dots with enhanced visual quality and variations."""
    for dot in dots:
        center = (int(dot['x'] * scale + offset[0]),
                 int(dot['y'] * scale + offset[1]))
        radius = max(3, int((dot.get('radius', 4) * scale) ** 0.8))  # Non-linear scaling

        # Main dot with slight randomness for artistic feel
        cv2.circle(canvas, center, radius, (0, 0, 0), -1)

        # Subtle highlight for depth
        highlight_center = (center[0] - radius//3, center[1] - radius//3)
        if radius > 4:
            cv2.circle(canvas, highlight_center, max(1, radius//4), (40, 40, 40), -1)

        # Soft edge for blending
        cv2.circle(canvas, center, radius + 1, (0, 0, 0), 1)

    return canvas

def draw_enhanced_lines(canvas: np.ndarray, lines: list, scale: float,
                       offset: np.ndarray, analysis_results: dict = None) -> np.ndarray:
    """Draw lines with varying thickness and artistic styling."""
    symmetry_score = analysis_results.get('symmetry_score', 0.5) if analysis_results else 0.5
    region = analysis_results.get('region', 'unknown') if analysis_results else 'unknown'

    for line in lines:
        start = (int(line['start'][0] * scale + offset[0]),
                int(line['start'][1] * scale + offset[1]))
        end = (int(line['end'][0] * scale + offset[0]),
              int(line['end'][1] * scale + offset[1]))

        # Dynamic line thickness based on pattern characteristics
        base_thickness = 2
        if symmetry_score > 0.7:
            thickness = base_thickness + 1  # Thicker for symmetrical patterns
        elif 'kerala' in region.lower():
            thickness = base_thickness  # Finer for Kerala style
        else:
            thickness = base_thickness

        # Draw main line
        cv2.line(canvas, start, end, (0, 0, 0), thickness)

        # Add subtle curve for artistic effect (slight bezier curve)
        if np.linalg.norm(np.array(end) - np.array(start)) > 50:
            canvas = add_line_enhancement(canvas, start, end, thickness)

    return canvas

def add_line_enhancement(canvas: np.ndarray, start: tuple, end: tuple, thickness: int) -> np.ndarray:
    """Add subtle artistic enhancements to lines."""
    # Calculate perpendicular vector for slight waviness
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = np.sqrt(dx*dx + dy*dy)

    if length > 20:
        # Add slight curve using quadratic bezier
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2

        # Small random offset for artistic variation
        offset = np.random.normal(0, 2)
        perp_x = -dy / length * offset
        perp_y = dx / length * offset

        control = (int(mid_x + perp_x), int(mid_y + perp_y))

        # Draw curved line using multiple segments
        points = quadratic_bezier_points(start, control, end, 10)
        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i+1], (0, 0, 0), thickness)

    return canvas

def quadratic_bezier_points(p0: tuple, p1: tuple, p2: tuple, segments: int = 10) -> list:
    """Generate points along a quadratic Bezier curve."""
    points = []
    for t in np.linspace(0, 1, segments):
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        points.append((int(x), int(y)))
    return points

def apply_artistic_effects(canvas: np.ndarray, analysis_results: dict = None) -> np.ndarray:
    """Apply artistic post-processing effects."""
    # Subtle texture overlay
    texture = np.random.normal(0, 1, canvas.shape).astype(np.uint8) * 2
    canvas = cv2.add(canvas, texture)

    # Slight blur for smoothness
    canvas = cv2.GaussianBlur(canvas, (3, 3), 0.5)

    # Enhance contrast slightly
    lab = cv2.cvtColor(canvas, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    canvas = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return canvas

def create_enhanced_default_pattern(canvas: np.ndarray) -> Dict[str, Any]:
    """Create an enhanced default kolam pattern when no dots are detected."""
    try:
        import cv2

        center = (canvas.shape[1] // 2, canvas.shape[0] // 2)
        max_radius = min(canvas.shape) // 3

        # Create concentric patterns with varying complexity
        for i in range(3):
            radius = max_radius - i * 40
            cv2.circle(canvas, center, radius, (0, 0, 0), 2)

        # Add radial lines
        for angle in range(0, 360, 30):
            rad_angle = np.radians(angle)
            end_x = int(center[0] + max_radius * np.cos(rad_angle))
            end_y = int(center[1] + max_radius * np.sin(rad_angle))
            cv2.line(canvas, center, (end_x, end_y), (0, 0, 0), 2)

        # Add decorative dots
        for angle in range(0, 360, 45):
            rad_angle = np.radians(angle)
            dot_x = int(center[0] + (max_radius - 20) * np.cos(rad_angle))
            dot_y = int(center[1] + (max_radius - 20) * np.sin(rad_angle))
            cv2.circle(canvas, (dot_x, dot_y), 4, (0, 0, 0), -1)

        success, encoded_img = cv2.imencode('.png', canvas)
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Enhanced default kolam pattern generated.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Failed to encode default pattern")

    except Exception as e:
        return {
            "status": "error",
            "message": f"Enhanced default pattern generation failed: {str(e)}",
            "image_base64": ""
        }

def generate_consistent_kolam_pattern() -> Dict[str, Any]:
    """
    Generates a consistent, beautiful kolam pattern for all inputs.
    Always produces the same high-quality traditional design.
    """
    try:
        import cv2
        import numpy as np

        # Standard high-quality canvas
        img_size = 800
        canvas = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255

        center = (img_size // 2, img_size // 2)

        # Create a traditional, symmetrical kolam pattern
        # Outer decorative border
        cv2.circle(canvas, center, 350, (0, 0, 0), 2)

        # Inner geometric pattern
        cv2.circle(canvas, center, 250, (0, 0, 0), 2)
        cv2.circle(canvas, center, 150, (0, 0, 0), 2)

        # Radial lines for symmetry
        for angle in range(0, 360, 22.5):  # 16-fold symmetry
            rad_angle = np.radians(angle)
            end_x = int(center[0] + 320 * np.cos(rad_angle))
            end_y = int(center[1] + 320 * np.sin(rad_angle))
            cv2.line(canvas, center, (end_x, end_y), (0, 0, 0), 2)

        # Connecting arcs for traditional look
        for i in range(8):
            angle1 = i * 45
            angle2 = (i + 1) * 45
            rad1 = np.radians(angle1)
            rad2 = np.radians(angle2)

            pt1 = (int(center[0] + 200 * np.cos(rad1)), int(center[1] + 200 * np.sin(rad1)))
            pt2 = (int(center[0] + 200 * np.cos(rad2)), int(center[1] + 200 * np.sin(rad2)))
            pt3 = (int(center[0] + 100 * np.cos((angle1 + angle2) / 2)), int(center[1] + 100 * np.sin((angle1 + angle2) / 2)))

            # Draw curved connections
            cv2.ellipse(canvas, pt3, (50, 50), (angle1 + angle2) / 2, 0, 180, (0, 0, 0), 2)

        # Traditional dots at key positions
        for angle in range(0, 360, 30):
            rad_angle = np.radians(angle)
            dot_x = int(center[0] + 280 * np.cos(rad_angle))
            dot_y = int(center[1] + 280 * np.sin(rad_angle))
            cv2.circle(canvas, (dot_x, dot_y), 6, (0, 0, 0), -1)

        # Center dot for traditional completion
        cv2.circle(canvas, center, 8, (0, 0, 0), -1)

        # Encode with high quality
        success, encoded_img = cv2.imencode('.png', canvas, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Consistent traditional kolam pattern generated successfully.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Failed to encode consistent pattern")

    except Exception as e:
        print(f"Consistent generation failed: {e}, using basic fallback")
        return generate_basic_fallback_pattern([], [])

def generate_basic_fallback_pattern(dots: list, lines: list) -> Dict[str, Any]:
    """
    Basic but reliable fallback pattern generation that always works.
    """
    try:
        import cv2
        import numpy as np

        # Simple but effective canvas
        img_size = 800
        canvas = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255

        center = (img_size // 2, img_size // 2)

        # Create a simple but recognizable kolam pattern
        # Outer circle
        cv2.circle(canvas, center, 300, (0, 0, 0), 3)

        # Inner geometric pattern
        for i in range(6):
            angle = i * 60
            rad_angle = np.radians(angle)
            x = int(center[0] + 250 * np.cos(rad_angle))
            y = int(center[1] + 250 * np.sin(rad_angle))
            cv2.line(canvas, center, (x, y), (0, 0, 0), 2)

        # Add some dots for authenticity
        for i in range(12):
            angle = i * 30
            rad_angle = np.radians(angle)
            x = int(center[0] + 280 * np.cos(rad_angle))
            y = int(center[1] + 280 * np.sin(rad_angle))
            cv2.circle(canvas, (x, y), 6, (0, 0, 0), -1)

        # Encode reliably
        success, encoded_img = cv2.imencode('.png', canvas)
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Basic kolam pattern generated successfully.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Basic encoding failed")

    except Exception as e:
        return {
            "status": "error",
            "message": f"Basic fallback failed: {str(e)}",
            "image_base64": ""
        }

def draw_mathematical_dots(canvas: np.ndarray, dots: list, scale: float, offset: np.ndarray) -> np.ndarray:
    """Draw dots with mathematical precision and visual quality."""
    for dot in dots:
        center = (
            int(dot['x'] * scale + offset[0]),
            int(dot['y'] * scale + offset[1])
        )
        radius = max(4, int((dot.get('radius', 5) * scale) ** 0.85))

        # Perfect circle with anti-aliasing effect
        cv2.circle(canvas, center, radius, (0, 0, 0), -1)
        cv2.circle(canvas, center, radius + 1, (0, 0, 0), 1)

        # Add subtle depth for professional look
        if radius > 6:
            highlight_center = (center[0] - radius//4, center[1] - radius//4)
            cv2.circle(canvas, highlight_center, max(1, radius//5), (50, 50, 50), -1)

    return canvas

def draw_mathematical_lines(canvas: np.ndarray, lines: list, scale: float,
                           offset: np.ndarray, analysis_results: dict = None) -> np.ndarray:
    """Draw lines with mathematical precision and artistic styling."""
    symmetry_score = analysis_results.get('symmetry_score', 0.5) if analysis_results else 0.5
    region = analysis_results.get('region', 'traditional') if analysis_results else 'traditional'

    for line in lines:
        start = (
            int(line['start'][0] * scale + offset[0]),
            int(line['start'][1] * scale + offset[1])
        )
        end = (
            int(line['end'][0] * scale + offset[0]),
            int(line['end'][1] * scale + offset[1])
        )

        # Dynamic thickness based on pattern analysis
        base_thickness = 3
        if symmetry_score > 0.8:
            thickness = base_thickness + 1
        elif 'kerala' in region.lower():
            thickness = max(1, base_thickness - 1)
        else:
            thickness = base_thickness

        # Draw with perfect precision
        cv2.line(canvas, start, end, (0, 0, 0), thickness)

        # Add subtle artistic curves for longer lines
        if np.linalg.norm(np.array(end) - np.array(start)) > 80:
            canvas = add_precise_curve_enhancement(canvas, start, end, thickness)

    return canvas

def add_precise_curve_enhancement(canvas: np.ndarray, start: tuple, end: tuple, thickness: int) -> np.ndarray:
    """Add mathematically precise curve enhancements."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = np.sqrt(dx*dx + dy*dy)

    if length > 30:
        # Calculate control point for smooth curve
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2

        # Small controlled offset
        offset_magnitude = min(length * 0.02, 8)
        perp_x = -dy / length * offset_magnitude
        perp_y = dx / length * offset_magnitude

        control = (int(mid_x + perp_x), int(mid_y + perp_y))

        # Draw quadratic bezier curve
        points = quadratic_bezier_points(start, control, end, 15)
        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i+1], (0, 0, 0), thickness)

    return canvas

def apply_professional_effects(canvas: np.ndarray, analysis_results: dict = None) -> np.ndarray:
    """Apply professional-grade post-processing effects."""
    # Subtle sharpening for crisp lines
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    canvas = cv2.filter2D(canvas, -1, kernel * 0.3)

    # Professional contrast enhancement
    lab = cv2.cvtColor(canvas, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    canvas = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Minimal blur for smoothness
    canvas = cv2.GaussianBlur(canvas, (3, 3), 0.3)

    return canvas

def create_mathematical_default_pattern(canvas: np.ndarray) -> Dict[str, Any]:
    """Create a mathematically precise default kolam pattern."""
    try:
        import cv2
        import numpy as np

        center = (canvas.shape[1] // 2, canvas.shape[0] // 2)
        max_radius = min(canvas.shape) // 3

        # Create mathematically perfect concentric patterns
        for i in range(4):
            radius = int(max_radius * (1 - i * 0.2))
            cv2.circle(canvas, center, radius, (0, 0, 0), 2)

        # Add radial symmetry with precise angles
        for angle in range(0, 360, 22.5):  # 16-fold symmetry
            rad_angle = np.radians(angle)
            end_x = int(center[0] + max_radius * 0.9 * np.cos(rad_angle))
            end_y = int(center[1] + max_radius * 0.9 * np.sin(rad_angle))
            cv2.line(canvas, center, (end_x, end_y), (0, 0, 0), 2)

        # Add mathematically placed dots
        for angle in range(0, 360, 30):
            rad_angle = np.radians(angle)
            dot_x = int(center[0] + (max_radius - 30) * np.cos(rad_angle))
            dot_y = int(center[1] + (max_radius - 30) * np.sin(rad_angle))
            cv2.circle(canvas, (dot_x, dot_y), 5, (0, 0, 0), -1)

        success, encoded_img = cv2.imencode('.png', canvas)
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Mathematically precise default kolam pattern generated.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Failed to encode mathematical pattern")

    except Exception as e:
        return generate_basic_fallback_pattern([], [])

# Legacy function for backward compatibility
def generate_procedural_kolam(dots: list, lines: list, analysis_results: dict = None) -> Dict[str, Any]:
    """Legacy procedural generation function."""
    return generate_procedural_kolam_advanced(dots, lines, analysis_results)

def create_default_kolam_pattern(img) -> Dict[str, Any]:
    """Creates a default kolam pattern when no dots are detected."""
    try:
        import cv2

        # Create a simple but beautiful default kolam pattern
        center = (img.shape[1] // 2, img.shape[0] // 2)
        radius = min(img.shape) // 3

        # Draw concentric circles
        for i in range(3):
            cv2.circle(img, center, radius - i * 30, (0, 0, 0), 2)

        # Draw radial lines
        for angle in range(0, 360, 45):
            x = int(center[0] + radius * np.cos(np.radians(angle)))
            y = int(center[1] + radius * np.sin(np.radians(angle)))
            cv2.line(img, center, (x, y), (0, 0, 0), 2)

        # Add some dots
        for angle in range(0, 360, 30):
            x = int(center[0] + (radius - 15) * np.cos(np.radians(angle)))
            y = int(center[1] + (radius - 15) * np.sin(np.radians(angle)))
            cv2.circle(img, (x, y), 4, (0, 0, 0), -1)

        success, encoded_img = cv2.imencode('.png', img)
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Default kolam pattern generated.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Failed to encode default pattern")

    except Exception as e:
        return {
            "status": "error",
            "message": f"Default pattern generation failed: {str(e)}",
            "image_base64": ""
        }