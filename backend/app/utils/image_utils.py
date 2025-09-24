import base64
import numpy as np
import cv2
from PIL import Image
import io

def decode_image(file) -> np.ndarray:
    """Decodes a file object into an OpenCV-compatible image format (BGR)."""
    try:
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        # Convert from PIL's RGB to OpenCV's BGR
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Could not decode image from file: {e}")

def decode_image_from_b64(base64_string: str) -> np.ndarray:
    """Decodes a base64 string into an OpenCV-compatible image format (BGR)."""
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        # Convert from PIL's RGB to OpenCV's BGR
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        # Consider logging this error
        raise ValueError(f"Could not decode image from base64 string: {e}")

def encode_image_to_bytes(image_array: np.ndarray) -> bytes:
    """Encodes an OpenCV image array (BGR) to PNG bytes."""
    try:
        # Convert BGR to RGB for PIL
        rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        return buffer.getvalue()
    except Exception as e:
        raise ValueError(f"Could not encode image to bytes: {e}")