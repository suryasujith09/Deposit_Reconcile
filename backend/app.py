from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from main import process_deposit_slip

# === Flask Setup ===
app = Flask(__name__)
CORS(app)  # Enables requests from React (http://localhost:3000)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# === Load API Keys ===
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VISION_API_KEY = os.getenv("VISION_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bank Slip OCR API is running!"})

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(image_path)

    try:
        result = process_deposit_slip(image_path, GEMINI_API_KEY, VISION_API_KEY)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
