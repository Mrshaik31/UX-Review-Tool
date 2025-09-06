import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO

# Local analyzers package
from analyzers.image_processor import ImageProcessor
from analyzers.text_extractor import TextExtractor
from analyzers.button_detector import ButtonDetector
from analyzers.scorer import UXScorer

# App setup
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])  # allow frontend dev
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# Health route
@app.route("/api/health", methods=["GET"])
def health_check():
    import cv2
    return jsonify({"status": "healthy", "opencv_version": cv2.__version__})

# Main analyze route
@app.route("/api/analyze", methods=["POST"])
def analyze_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image provided (form key must be 'image')"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No image selected"}), 400

        # Read file directly into memory (no saving to disk)
        image_data = file.read()

        # Initialize processors
        image_processor = ImageProcessor()
        text_extractor = TextExtractor()
        button_detector = ButtonDetector()
        scorer = UXScorer()

        # Preprocess image
        image = image_processor.preprocess_image(image_data)

        # Extract elements
        text_elements = text_extractor.extract_text(image)
        buttons = button_detector.detect_buttons(image, text_elements)

        # Calculate scores
        scores = scorer.calculate_scores(image, text_elements, buttons)
        recommendations = scorer.generate_recommendations(scores, text_elements, buttons)

        # Response
        response = {
            "screenshot_id": f"img_{abs(hash(str(image_data))) % 100000}",
            "filename": file.filename.replace(" ", "_"),
            "overall_score": scores.get("overall"),
            "detailed_scores": {
                "cta_prominence": round(scores.get("cta_prominence", 0), 2),
                "visual_hierarchy": round(scores.get("visual_hierarchy", 0), 2),
                "accessibility": round(scores.get("accessibility", 0), 2),
                "color_contrast": round(scores.get("color_contrast", 0), 2),
            },
            "elements_detected": {
                "buttons": len(buttons),
                "text_blocks": len(text_elements),
                "images": scores.get("image_count", 0)
            },
            "issues": recommendations.get("issues", []),
            "recommendations": recommendations.get("suggestions", []),
        }

        return jsonify(response)

    except Exception as e:
        print("Error during analysis:", e)
        print(traceback.format_exc())
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    print("Starting UX Review Tool Backend (No File Saving)...")
    app.run(debug=True, host="0.0.0.0", port=5000)
