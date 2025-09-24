from flask import request, jsonify, current_app
from flask_mail import Message
from . import api  # Imports the 'api' blueprint from the __init__.py in the same folder
from ..services import vision_service, ai_service
from ..utils import image_utils
from .. import mail
import google.api_core.exceptions
import base64

@api.route('/chat', methods=['POST'])
def handle_chat():
    """
    Main chat endpoint. Handles both text-only queries and image uploads.
    It robustly checks for data in both multipart/form-data and application/json.
    """
    # --- Enhanced Debugging: Log incoming request details ---
    current_app.logger.info(f"Received request for /api/chat with Content-Type: {request.content_type}")
    current_app.logger.info(f"Form data received: {request.form.to_dict()}")
    current_app.logger.info(f"Files received: {request.files.to_dict()}")
    # Use silent=True to prevent an error if the body is not JSON
    current_app.logger.info(f"JSON data received: {request.get_json(silent=True)}")
    # --- End of Debugging ---

    prompt = None
    image_file = None

    # Handle both multipart/form-data and JSON requests
    prompt = None
    image_data = None

    if request.content_type.startswith('multipart/form-data'):
        prompt = request.form.get('prompt')
        image_file = request.files.get('image')
        if image_file:
            image_data = image_file
    elif request.is_json:
        data = request.get_json()
        prompt = data.get('prompt')
        image_data = data.get('image_data')  # base64 string

    # If no prompt was found and no image, return an error
    if not prompt and not image_data:
        error_msg = "No 'prompt' field or 'image_data' found in request."
        current_app.logger.error(error_msg)
        return jsonify({'error': error_msg}), 400

    try:
        if image_data:
            # --- Handle Image + Text Query ---
            if isinstance(image_data, str):  # base64
                image_array = image_utils.decode_image_from_b64(image_data)
            else:  # file object
                image_array = image_utils.decode_image(image_data)
            if image_array is None:
                return jsonify({'error': 'Invalid or unsupported image format'}), 400

            # 1. Get a detailed analysis from the vision service
            analysis_report, final_pattern = vision_service.analyze_kolam_image(image_array)

            # 2. Pass the report and original prompt to the AI service
            final_response = ai_service.get_ai_response_with_vision(prompt, analysis_report)

        else:
            # --- Handle Text-Only Query ---
            final_response = ai_service.get_ai_response(prompt)
        
        return jsonify({'response': final_response})

    except google.api_core.exceptions.InvalidArgument as e:
        # Handle invalid API key
        if "API_KEY_INVALID" in str(e):
            return jsonify({'error': 'Invalid Google Gemini API key. Please check your API key in the backend/.env file and ensure it is valid.'}), 400
        else:
            current_app.logger.error(f"An error occurred in /chat: {e}", exc_info=True)
            return jsonify({'error': 'An internal server error occurred'}), 500
    except google.api_core.exceptions.ResourceExhausted as e:
        # Handle quota exceeded
        return jsonify({'error': 'API quota exceeded. Please check your Google Gemini API plan and billing details.'}), 429
    except Exception as e:
        # Log the error for debugging
        current_app.logger.error(f"An error occurred in /chat: {e}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred'}), 500

@api.route('/analyze_kolam', methods=['POST'])
def analyze_kolam():
    """
    Endpoint for analyzing a kolam image and generating a digital regeneration.
    Expects JSON with 'image_data' as base64 string.
    """
    current_app.logger.info("Received request for /api/analyze_kolam")

    data = request.get_json()
    image_data = data.get('image_data')

    if not image_data:
        return jsonify({'error': 'No image_data provided'}), 400

    try:
        # Decode the base64 image
        image_array = image_utils.decode_image_from_b64(image_data)
        if image_array is None:
            return jsonify({'error': 'Invalid or unsupported image format'}), 400

        # 1. Analyze the image
        analysis_results, final_pattern = vision_service.analyze_kolam_image(image_array)

        # 2. Generate a description using AI
        description_dict = ai_service.generate_kolam_description(analysis_results)

        # 3. Generate digital recreation using detected dots and lines
        # Extract dots and lines from the pattern
        dots_data = [{'x': dot.x, 'y': dot.y, 'radius': dot.radius} for dot in final_pattern.dots]
        lines_data = [{'start': line.p1, 'end': line.p2} for line in final_pattern.lines]

        image_result = ai_service.generate_kolam_image(dots_data, lines_data, analysis_results)
        if image_result['status'] == 'success':
            regenerated_image_b64 = image_result['image_base64']
        else:
            regenerated_image_b64 = ""  # Placeholder for failed generation

        # 4. Encode original image back to base64 for response
        original_image_b64 = base64.b64encode(image_utils.encode_image_to_bytes(image_array)).decode('utf-8')
        original_image_data_url = f"data:image/png;base64,{original_image_b64}"

        # 5. Prepare response
        response = {
            'original_image': original_image_data_url,
            'analysis': analysis_results,
            'description': description_dict,
            'regenerated_image': f"data:image/png;base64,{regenerated_image_b64}"
        }

        return jsonify(response)

    except google.api_core.exceptions.InvalidArgument as e:
        if "API_KEY_INVALID" in str(e):
            return jsonify({'error': 'Invalid Google Gemini API key. Please check your API key in the backend/.env file and ensure it is valid.'}), 400
        else:
            current_app.logger.error(f"An error occurred in /analyze_kolam: {e}", exc_info=True)
            return jsonify({'error': 'An internal server error occurred'}), 500
    except google.api_core.exceptions.ResourceExhausted as e:
        return jsonify({'error': 'API quota exceeded. Please check your Google Gemini API plan and billing details.'}), 429
    except Exception as e:
        current_app.logger.error(f"An error occurred in /analyze_kolam: {e}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred'}), 500

@api.route('/contact', methods=['POST'])
def handle_contact():
    """
    Handle contact form submissions and send email notifications.
    """
    current_app.logger.info("Received contact form submission")

    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        full_name = data.get('fullName', '').strip()
        email = data.get('email', '').strip()
        category = data.get('category', '').strip()

        # Validate required fields
        if not full_name or not email or not category:
            return jsonify({'error': 'All fields are required'}), 400

        # Create email message
        msg = Message(
            subject=f'New KolamGPT Contact Form Submission - {category}',
            recipients=[current_app.config['CONTACT_RECIPIENT']],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )

        # Email body
        msg.body = f"""
New contact form submission from KolamGPT website:

Name: {full_name}
Email: {email}
Category: {category}

---
This email was sent from the KolamGPT contact form.
"""

        # Send email
        mail.send(msg)

        current_app.logger.info(f"Contact form email sent successfully for {full_name} ({email})")

        return jsonify({
            'message': 'Thank you for your message! We\'ll get back to you soon.',
            'success': True
        })

    except Exception as e:
        current_app.logger.error(f"Error sending contact form email: {e}", exc_info=True)
        return jsonify({'error': 'Failed to send message. Please try again later.'}), 500