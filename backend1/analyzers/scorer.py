import numpy as np
import cv2

class UXScorer:
    def __init__(self):
        print("UXScorer initialized")

    def calculate_scores(self, image, text_elements, buttons):
        try:
            scores = {}
            scores["cta_prominence"] = self._calculate_cta_prominence(image, buttons)
            scores["visual_hierarchy"] = self._calculate_visual_hierarchy(text_elements)
            scores["accessibility"] = self._calculate_accessibility(image, text_elements, buttons)
            scores["color_contrast"] = self._calculate_color_contrast(image, buttons)

            # weighted average
            weights = {
                'cta_prominence': 0.3,
                'visual_hierarchy': 0.25,
                'accessibility': 0.25,
                'color_contrast': 0.2
            }
            weighted = sum(scores[k] * weights[k] for k in weights)
            scores["overall"] = max(45, min(95, int(weighted * 100)))

            # ✅ Boost score if all metrics are good
            if (scores["cta_prominence"] >= 0.6 and 
                scores["visual_hierarchy"] >= 0.6 and 
                scores["accessibility"] >= 0.7 and 
                scores["color_contrast"] >= 0.65):
                scores["overall"] = max(scores["overall"], 80)

            scores["image_count"] = self._count_images(image)
            return scores
        except Exception as e:
            print("Error calculating scores:", e)
            return {
                "cta_prominence": 0.6, "visual_hierarchy": 0.7,
                "accessibility": 0.6, "color_contrast": 0.65,
                "overall": 65, "image_count": 1
            }

    def _calculate_cta_prominence(self, image, buttons):
        if not buttons:
            return 0.4
        cta_buttons = [b for b in buttons if b.get("type") == "cta"]
        if not cta_buttons:
            return 0.5

        main_cta = max(cta_buttons, key=lambda x: x.get("area", 0))
        h, w = image.shape[:2]
        viewport_area = h * w

        # size factor
        size_ratio = main_cta.get("area", 0) / (viewport_area + 1e-9)
        size_score = min(size_ratio * 200, 1.0)

        # position factor (closer to center-top = better)
        center_x, ideal_y = w // 2, h // 3
        cta_cx = main_cta["x"] + main_cta["width"] // 2
        cta_cy = main_cta["y"] + main_cta["height"] // 2
        dist = np.sqrt((cta_cx - center_x) ** 2 + (cta_cy - ideal_y) ** 2)
        max_dist = np.sqrt((w // 2) ** 2 + (h // 2) ** 2)
        position_score = max(0.3, 1 - (dist / (max_dist + 1e-9)))

        return min(1.0, (size_score * 0.6) + (position_score * 0.4))

    def _calculate_visual_hierarchy(self, text_elements):
        if len(text_elements) < 2:
            return 0.5
        heights = [el["height"] for el in text_elements if el["height"] > 5]
        if not heights:
            return 0.5
        unique_sizes = len(set(heights))
        size_range = max(heights) - min(heights) if heights else 0
        size_variety_score = min(unique_sizes / 5.0, 1.0)
        size_range_score = min(size_range / 30.0, 1.0)
        return (size_variety_score * 0.6) + (size_range_score * 0.4)

    def _calculate_accessibility(self, image, text_elements, buttons):
        score = 0.5
        if text_elements:
            small_count = sum(1 for el in text_elements if el["height"] < 12)
            small_ratio = small_count / len(text_elements)
            if small_ratio < 0.3:
                score += 0.2
            elif small_ratio < 0.6:
                score += 0.1
        if buttons:
            accessible_buttons = sum(1 for b in buttons if b["width"] >= 44 and b["height"] >= 30)
            button_accessibility = accessible_buttons / len(buttons)
            score += button_accessibility * 0.3
        return min(score, 1.0)

    def _calculate_color_contrast(self, image, buttons):
        if not buttons:
            return 0.6
        contrasts = []
        for b in buttons:
            try:
                roi = image[b["y"]:b["y"]+b["height"], b["x"]:b["x"]+b["width"]]
                if roi.size == 0:
                    continue
                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                bg_lum = float(roi_gray.mean())
                text_lum = 0.0 if bg_lum > 128 else 255.0
                lighter = max(bg_lum, text_lum) / 255.0
                darker = min(bg_lum, text_lum) / 255.0
                contrast_ratio = (lighter + 0.05) / (darker + 0.05)
                normalized = min(contrast_ratio / 4.5, 1.0)
                contrasts.append(normalized)
            except Exception:
                continue
        return float(np.mean(contrasts)) if contrasts else 0.6

    def _count_images(self, image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            count = 0
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                if w > 100 and h > 100:
                    count += 1
            return min(count, 5)
        except:
            return 1

    def generate_recommendations(self, scores, text_elements, buttons):
        issues = []
        suggestions = []
        try:
            # ✅ Tiered CTA recommendations
            cta_score = scores.get("cta_prominence", 0)
            if cta_score < 0.6:
                issues.append({"type": "cta_prominence", "reason": "low_cta"})

                if cta_score < 0.2:
                    suggestions.append({
                        "title": "Critical: Add a Strong CTA",
                        "description": "Your landing page is missing a clear call-to-action or it’s nearly invisible. "
                                       "Add a bold, noticeable CTA button at the top section (‘above the fold’). "
                                       "Use a bright color like green, blue, or orange with strong text such as ‘Get Started’ or ‘Book Now’.",
                        "css_fix": "button.cta { font-size:20px; padding:16px 32px; background:#28a745; color:#fff; border-radius:10px; font-weight:bold; }",
                        "priority": "critical"
                    })
                elif cta_score < 0.4:
                    suggestions.append({
                        "title": "Improve CTA Visibility",
                        "description": "Your call-to-action exists but is too weak. Increase its size, add more padding, "
                                       "and ensure it has enough visual weight. Place it higher on the page to draw attention.",
                        "css_fix": "button.cta { font-size:18px; padding:14px 28px; background:#ff5722; color:#fff; border-radius:8px; }",
                        "priority": "high"
                    })
                else:  # 0.4 ≤ score < 0.6
                    suggestions.append({
                        "title": "Make CTA Stand Out More",
                        "description": "Your CTA is visible but not prominent enough. Try using a more contrasting color, "
                                       "increasing its size slightly, or giving it more spacing from surrounding elements.",
                        "css_fix": "button.cta { background:#007BFF; font-size:16px; padding:12px 24px; border-radius:6px; }",
                        "priority": "medium"
                    })

            if scores.get("visual_hierarchy", 0) < 0.6:
                suggestions.append({
                    "title": "Improve Text Hierarchy",
                    "description": "Use larger headings (h1, h2) for important text and smaller sizes for body content. "
                                   "This helps guide users’ attention.",
                    "css_fix": "h1{font-size:2rem;font-weight:700} p{font-size:1rem;color:#444}",
                    "priority": "medium"
                })

            if scores.get("accessibility", 0) < 0.7:
                issues.append({"type": "accessibility", "reason": "small_text_or_buttons"})
                suggestions.append({
                    "title": "Enhance Accessibility",
                    "description": "Some text or buttons are too small. Increase font size to at least 14px "
                                   "and make buttons at least 44x44px for touch devices.",
                    "css_fix": "button{min-height:44px; min-width:44px; font-size:14px}",
                    "priority": "medium"
                })

            if scores.get("color_contrast", 0) < 0.65:
                issues.append({"type": "contrast", "reason": "low_contrast"})
                suggestions.append({
                    "title": "Improve Color Contrast",
                    "description": "Text and background colors have low contrast. "
                                   "Ensure the contrast ratio meets WCAG 2.1 standards (4.5:1 for normal text).",
                    "css_fix": "body{color:#222;background:#fff}",
                    "priority": "high"
                })

            # ✅ Show success message only when score is high
            if scores.get("overall", 0) >= 80:
                suggestions.append({
                    "title": "Nice Work!",
                    "description": "Your design has good fundamentals. Keep refining by testing with real users."
                })

            return {"issues": issues, "suggestions": suggestions}

        except Exception as e:
            print("Recommendation gen error:", e)
            return {"issues": [], "suggestions": []}
