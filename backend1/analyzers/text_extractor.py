# backend/analyzers/text_extractor.py
import os
import platform
import pytesseract
import cv2

class TextExtractor:
    def __init__(self):
        # Attempt to find Tesseract on Windows if not in PATH
        if platform.system() == "Windows":
            possible_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    pytesseract.pytesseract.tesseract_cmd = p
                    print(f"Found tesseract at: {p}")
                    break
            else:
                print("Warning: Tesseract not found in common paths. Ensure tesseract.exe is installed and in PATH.")
        print("TextExtractor initialized")

    def extract_text(self, image):
        """Return list of text elements with bounding boxes using pytesseract."""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Improve contrast for OCR
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config='--psm 6')
            text_elements = []
            for i, txt in enumerate(data.get("text", [])):
                txt = (txt or "").strip()
                conf = data.get("conf", [])[i] if "conf" in data else "-1"
                try:
                    conf_val = float(conf)
                except:
                    conf_val = -1.0
                if txt and len(txt) > 1 and conf_val > 30:
                    text_elements.append({
                        "text": txt,
                        "x": int(data["left"][i]),
                        "y": int(data["top"][i]),
                        "width": int(data["width"][i]),
                        "height": int(data["height"][i]),
                        "confidence": conf_val
                    })
            return text_elements
        except Exception as e:
            print("Text extraction error:", e)
            return []
