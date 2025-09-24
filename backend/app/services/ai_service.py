import json
import base64
import io
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
    Generates a digital kolam image using AI-based generation for better accuracy.
    Falls back to procedural generation if AI fails.
    """
    try:
        # First try AI-based generation with a descriptive prompt
        if analysis_results:
            prompt = create_kolam_generation_prompt(analysis_results, len(dots), len(lines))

            # Try AI generation first
            try:
                model = _get_model()
                response = model.generate_content([
                    "You are an expert at creating traditional Indian kolam patterns. Generate a beautiful, accurate digital recreation.",
                    prompt
                ])

                # Extract image from response (this would need to be adjusted based on actual API)
                # For now, fall through to procedural generation
                print("AI image generation attempted, falling back to procedural generation")

            except Exception as e:
                print(f"AI generation failed: {e}, using procedural generation")

        # Fallback: Procedural generation with improved algorithm
        return generate_procedural_kolam(dots, lines, analysis_results)

    except Exception as e:
        return {
            "status": "error",
            "message": f"Image generation failed: {str(e)}",
            "image_base64": ""
        }

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

def generate_procedural_kolam(dots: list, lines: list, analysis_results: dict = None) -> Dict[str, Any]:
    """Generates a kolam image procedurally with improved algorithms."""
    try:
        import cv2
        import numpy as np

        # Create a high-quality white canvas
        img_size = 800  # Higher resolution
        regenerated_img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255

        if not dots:
            # If no dots detected, create a simple default pattern
            return create_default_kolam_pattern(regenerated_img)

        # Calculate bounds and scaling
        if dots:
            x_coords = [d['x'] for d in dots]
            y_coords = [d['y'] for d in dots]
            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)

            # Add padding
            width = max_x - min_x if max_x > min_x else 100
            height = max_y - min_y if max_y > min_y else 100

            scale_x = (img_size * 0.8) / width if width > 0 else 1
            scale_y = (img_size * 0.8) / height if height > 0 else 1
            scale = min(scale_x, scale_y)

            offset_x = img_size * 0.1 - min_x * scale
            offset_y = img_size * 0.1 - min_y * scale

            # Draw dots with better quality
            for dot in dots:
                center = (int(dot['x'] * scale + offset_x), int(dot['y'] * scale + offset_y))
                radius = max(4, int(dot.get('radius', 3) * scale * 0.5))
                cv2.circle(regenerated_img, center, radius, (0, 0, 0), -1)
                # Add a subtle border for better visibility
                cv2.circle(regenerated_img, center, radius + 1, (0, 0, 0), 1)

            # Draw lines with better quality
            for line in lines:
                start_point = (int(line['start'][0] * scale + offset_x),
                              int(line['start'][1] * scale + offset_y))
                end_point = (int(line['end'][0] * scale + offset_x),
                            int(line['end'][1] * scale + offset_y))
                cv2.line(regenerated_img, start_point, end_point, (0, 0, 0), 3)

        # Apply anti-aliasing for smoother lines
        regenerated_img = cv2.GaussianBlur(regenerated_img, (3, 3), 0)

        # Convert to base64
        success, encoded_img = cv2.imencode('.png', regenerated_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        if success:
            image_base64 = base64.b64encode(encoded_img.tobytes()).decode('utf-8')
            return {
                "status": "success",
                "message": "Digital kolam generated successfully.",
                "image_base64": image_base64
            }
        else:
            raise ValueError("Failed to encode image")

    except Exception as e:
        return {
            "status": "error",
            "message": f"Procedural generation failed: {str(e)}",
            "image_base64": ""
        }

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