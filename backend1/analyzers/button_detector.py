# backend/analyzers/button_detector.py
import cv2
import numpy as np

class ButtonDetector:
    def __init__(self):
        print("ButtonDetector initialized")

    def detect_buttons(self, image, text_elements):
        try:
            buttons = []
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            kernel = np.ones((3,3), np.uint8)
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if 30 < w < 1000 and 10 < h < 400:
                    aspect = w / (h + 1e-6)
                    if 1.2 < aspect < 8:
                        button_text = self._find_text_in_region(text_elements, x, y, w, h)
                        roi = image[y:y+h, x:x+w]
                        is_button_like = self._analyze_button_colors(roi)
                        if button_text or is_button_like:
                            buttons.append({
                                "x": x, "y": y, "width": w, "height": h,
                                "text": button_text or "",
                                "type": self._classify_button_type(button_text or ""),
                                "area": w * h
                            })
            # also detect small text-based potential buttons
            buttons.extend(self._detect_text_buttons(text_elements))
            buttons = self._remove_duplicate_buttons(buttons)
            return buttons
        except Exception as e:
            print("Button detection error:", e)
            return []

    def _find_text_in_region(self, text_elements, x, y, w, h):
        found = []
        for el in text_elements:
            cx = el["x"] + el["width"] // 2
            cy = el["y"] + el["height"] // 2
            if x <= cx <= x + w and y <= cy <= y + h:
                found.append(el["text"])
        return " ".join(found) if found else None

    def _analyze_button_colors(self, roi):
        if roi.size == 0 or roi.shape[0] < 4 or roi.shape[1] < 4:
            return False
        var = np.var(roi.reshape(-1, 3), axis=0)
        avg_var = np.mean(var)
        return avg_var < 2000

    def _classify_button_type(self, text):
        if not text:
            return "unknown"
        text_lower = text.lower()
        cta_keywords = ['buy','purchase','sign up','register','subscribe','get','start','try','download','join','order','shop','learn','contact','book']
        for k in cta_keywords:
            if k in text_lower:
                return "cta"
        return "navigation"

    def _is_button_text(self, text):
        if not text:
            return False
        indicators = ['click','tap','submit','send','next','back','continue','ok','yes','no']
        return any(i in text.lower() for i in indicators)

    def _detect_text_buttons(self, text_elements):
        buttons = []
        for el in text_elements:
            txt = el["text"]
            if len(txt) <= 20 and (self._is_button_text(txt) or len(txt.split()) <= 3):
                buttons.append({
                    "x": el["x"], "y": el["y"], "width": el["width"], "height": el["height"],
                    "text": txt, "type": self._classify_button_type(txt), "area": el["width"] * el["height"]
                })
        return buttons

    def _remove_duplicate_buttons(self, buttons):
        unique = []
        for b in buttons:
            dup = False
            for u in unique:
                overlap_x = max(0, min(b["x"]+b["width"], u["x"]+u["width"]) - max(b["x"], u["x"]))
                overlap_y = max(0, min(b["y"]+b["height"], u["y"]+u["height"]) - max(b["y"], u["y"]))
                if overlap_x > 10 and overlap_y > 5:
                    dup = True
                    break
            if not dup:
                unique.append(b)
        return unique
