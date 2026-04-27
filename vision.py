import cv2
import mss
import numpy as np
import pytesseract


# =========================
# 🖥️ SCREEN CAPTURE
# =========================
def capture_screen():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return frame
    except Exception as e:
        print("Screen Error:", e)
        return None


# =========================
# 🎥 CAMERA CAPTURE
# =========================
def capture_camera():
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return None

        ret, frame = cap.read()
        cap.release()

        return frame if ret else None

    except Exception as e:
        print("Camera Error:", e)
        return None


# =========================
# 🔤 OCR (TEXT EXTRACTION)
# =========================
def extract_text(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 🔥 Improve contrast
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        text = pytesseract.image_to_string(gray)

        return text.strip()

    except:
        return ""


# =========================
# 🧠 MAIN PROCESSOR
# =========================
def process_vision(frame):
    """
    Extract meaningful data from frame
    (currently OCR, later object detection)
    """

    text = extract_text(frame)

    # 🔥 If text found → priority
    if text and len(text) > 5:
        return f"Detected text:\n{text}"

    # 🔜 Future: object detection here
    return "No clear text detected. Possibly objects or visuals."