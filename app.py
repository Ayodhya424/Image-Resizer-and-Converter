from flask import Flask, request, render_template, send_file, after_this_request
from PIL import Image, UnidentifiedImageError
import os
import uuid
import pillow_avif  # AVIF support

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'avif', 'webp', 'bmp', 'tiff', 'ico', 'heif', 'heic'}

MAX_WIDTH = 1920
MAX_HEIGHT = 1080
MIN_WIDTH = 100
MIN_HEIGHT = 100


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("photo")

        if not file or not allowed_file(file.filename):
            return "Error: Unsupported or no file uploaded!"

        # Unique filename (multi-user safe)
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(filepath)

        try:
            with Image.open(filepath) as img:

                width = int(request.form["width"])
                height = int(request.form["height"])

                if width > MAX_WIDTH or height > MAX_HEIGHT:
                    return f"Error: Max allowed size {MAX_WIDTH}x{MAX_HEIGHT}"

                if width < MIN_WIDTH or height < MIN_HEIGHT:
                    return f"Error: Min allowed size {MIN_WIDTH}x{MIN_HEIGHT}"

                img = img.resize((width, height))

                resized_name = f"resized_{uuid.uuid4().hex}.png"
                resized_path = os.path.join(app.config["UPLOAD_FOLDER"], resized_name)
                img.save(resized_path, "PNG")

        except UnidentifiedImageError:
            return "Error: Unsupported or corrupted image file."
        except Exception as e:
            return f"Error: {str(e)}"

        # Delete files after sending
        @after_this_request
        def cleanup(response):
            try:
                os.remove(filepath)
                os.remove(resized_path)
            except Exception:
                pass
            return response

        return send_file(resized_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    # DEVELOPMENT MODE
    # app.run(debug=True)

    # PRODUCTION MODE
    app.run(host="0.0.0.0", port=5000)
    # To use development Mode comment out Production Mode

