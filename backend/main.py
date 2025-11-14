import cv2
import numpy as np
import os
import base64
import requests
import json
from google import genai
import re

# === Image Processing ===
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image '{image_path}' not found!")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    blur = cv2.GaussianBlur(enhanced, (5, 5), 0)
    _, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.adaptiveThreshold(
        otsu, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 3
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    resized = cv2.resize(morph, (1024, 1024))
    return resized


def encode_image(image):
    is_success, buffer = cv2.imencode(".jpg", image)
    if not is_success:
        raise RuntimeError("Could not encode image")
    return buffer.tobytes()


def vision_ocr(image_path, vision_api_key):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    url = f"https://vision.googleapis.com/v1/images:annotate?key={vision_api_key}"
    vision_req = {
        "requests": [{
            "image": {"content": encoded_image},
            "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
        }]
    }
    resp = requests.post(url, json=vision_req)
    result = resp.json()

    try:
        vision_text = result["responses"][0]["fullTextAnnotation"]["text"]
    except Exception:
        vision_text = ""

    return vision_text


def gemini_extract_json(client, img_bytes, vision_text):
    prompt = (
        "You are a data extraction expert for Indian bank deposit slips. "
        "Analyze the following image and OCR text to extract details as a JSON object ONLY in Camel Case.\n\n"
        "Required keys:\n"
        "- date (format: DD/MM/YY or DD/MM/YYYY)\n"
        "- branch (use full name if visible, else reasoned guess)\n"
        "- account_number\n"
        "- name (person or organization)\n"
        "- contact_number (try to infer from OCR if visible, else 'unknown')\n"
        "- amount (numerical, e.g., 21000)\n"
        "- amount_in_words (convert the number into words if not clearly visible in camel case)\n"
        "- cheque_details (if none, write 'self deposit' or 'cash')\n"
        "- signature (return name in camel case)\n\n"
        "If a value is missing, intelligently infer or approximate it from OCR text context rather than returning N/A.\n"
        "Return only clean JSON — no markdown formatting.\n\n"
        f"OCR TEXT:\n{vision_text}"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}},
                ],
            }
        ],
    )
    print("Gemini Response:", response)
    return response.text


def process_deposit_slip(image_path, gemini_api_key, vision_api_key):
    client = genai.Client(api_key=gemini_api_key)
    processed_image = preprocess_image(image_path)
    img_bytes = encode_image(processed_image)
    vision_text = vision_ocr(image_path, vision_api_key)
    gemini_response = gemini_extract_json(client, img_bytes, vision_text)

    # Clean JSON output
    cleaned = gemini_response.strip()
    cleaned = re.sub(r"```json|```", "", cleaned).strip()

    try:
        data = json.loads(cleaned)
        return data
    except Exception:
        return {"raw_response": cleaned}
