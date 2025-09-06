# backend/analyzers/image_processor.py
import io
import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        print("ImageProcessor initialized")

    def preprocess_image(self, image_data):
        """Convert uploaded image bytes to OpenCV image (BGR) and run basic preprocessing."""
        try:
            pil_image = Image.open(io.BytesIO(image_data))
            # convert to RGB if needed
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")
            # Resize if very large
            max_width = 1200
            if pil_image.width > max_width:
                ratio = max_width / pil_image.width
                new_h = int(pil_image.height * ratio)
                pil_image = pil_image.resize((max_width, new_h), Image.Resampling.LANCZOS)
            # convert to OpenCV BGR
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            # denoise
            cv_image = cv2.bilateralFilter(cv_image, d=9, sigmaColor=75, sigmaSpace=75)
            return cv_image
        except Exception as e:
            raise Exception(f"Failed to preprocess image: {e}")
