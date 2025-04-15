
from flask import Flask, request, render_template, url_for
import google.generativeai as genai
from PIL import Image
import os
import uuid

from dotenv import load_dotenv

app = Flask(__name__)

# Configure Gemini AI
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key = api_key)

model = genai.GenerativeModel("gemini-1.5-pro")

# Ensure upload directories exist
os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "image" not in request.files:
            return "No image uploaded", 400

        image_file = request.files["image"]
        
        # Generate a unique filename
        filename = f"{uuid.uuid4()}{os.path.splitext(image_file.filename)[1]}"
        file_path = os.path.join(app.root_path, 'static', 'uploads', filename)
        
        # Save the file
        image_file.save(file_path)
        
        # Open the image for analysis
        image = Image.open(file_path)

        # Define the AI prompt
        prompt = """You are a highly experienced radiologist with expertise in interpreting a wide range of radiology investigations..."""  # (Your detailed prompt here)

        # Send to Gemini AI
        response = model.generate_content([image, prompt])
        result_text = response.text

        return render_template("result.html", image_path=filename, result=result_text)

    return render_template("upload.html")  # Load the upload form

if __name__ == "__main__":
    # Load configuration from environment variables
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8080))

    app.run(debug=debug_mode, host=host, port=port)