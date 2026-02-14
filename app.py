from flask import Flask, request, render_template, send_file, after_this_request
from PIL import Image, UnidentifiedImageError
import os
import uuid
import pillow_avif  # Enables AVIF image support in Pillow

# Create Flask app
app = Flask(__name__)

# Folder where uploaded and resized images will be temporarily stored
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'avif', 'webp', 'bmp', 'tiff', 'ico', 'heif', 'heic'}

# Size limits for resizing
MAX_WIDTH = 1920  # Maximum width in pixels
MAX_HEIGHT = 1080  # Maximum height in pixels
MIN_WIDTH = 100    # Minimum width in pixels
MIN_HEIGHT = 100    # Manimum height in pixels


# Function to check if uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Main route (homepage)
@app.route("/", methods=["GET", "POST"])
def upload_file():

    # When user submits the form
    if request.method == "POST":
        file = request.files.get("photo")

        # Validate file
        if not file or not allowed_file(file.filename):
            return "Error: Unsupported or no file uploaded!"

        # Create unique filename so multiple users don't overwrite each other
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(filepath)

        try:
            # Open image using Pillow
            with Image.open(filepath) as img:

                # Get resize dimensions from form
                width = int(request.form["width"])
                height = int(request.form["height"])

                # Validate dimensions
                if width > MAX_WIDTH or height > MAX_HEIGHT:
                    return f"Error: Max allowed size {MAX_WIDTH}x{MAX_HEIGHT}"

                if width < MIN_WIDTH or height < MIN_HEIGHT:
                    return f"Error: Min allowed size {MIN_WIDTH}x{MIN_HEIGHT}"

                # Resize image
                img = img.resize((width, height))

                # Save resized image with new unique name
                resized_name = f"resized_{uuid.uuid4().hex}.png"
                resized_path = os.path.join(app.config["UPLOAD_FOLDER"], resized_name)
                img.save(resized_path, "PNG")

        except UnidentifiedImageError:
            return "Error: Unsupported or corrupted image file."
        except Exception as e:
            return f"Error: {str(e)}"

        # Automatically delete temporary files after sending download
        @after_this_request
        def cleanup(response):
            try:
                os.remove(filepath)
                os.remove(resized_path)
            except Exception:
                pass
            return response

        # Send resized image to user as automatic download
        return send_file(resized_path, as_attachment=True)

    # Show upload page
    return render_template("index.html")


if __name__ == "__main__":
    # DEVELOPMENT MODE (use while coding locally)
    # app.run(debug=True)

    # PRODUCTION MODE (Render / hosting)
    app.run(host="0.0.0.0", port=5000)

    # To use development Mode comment out Production Mode

