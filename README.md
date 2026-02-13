# PNG Image Resizer and Converter

This project provides a simple tool to resize PNG images and convert them into other formats (e.g., JPEG, BMP). 
It is built using Python and the Pillow library.

<img width="1880" height="1036" alt="Screenshot 2026-02-13 215535" src="https://github.com/user-attachments/assets/986f4482-0a35-4fff-83fc-8ce9c0f4ae0c" />

A simple web-based application that allows users to upload a photo, resize it to custom dimensions, and adjust the target file size. 
This tool is useful for preparing images for web uploads, email attachments, or any application where specific dimensions and file size are required.

---

## Features
- Upload PNG, JPEG, or other image formats
- Resize images to custom width and height (up to 1920x1080)
- Set a target file size (up to 2000 KB)
- Convert images to different formats (PNG, JPEG, etc.)
- Clean and user-friendly web interface

## Project Structure
<img width="663" height="397" alt="image" src="https://github.com/user-attachments/assets/aa7fc8e4-8b5c-4de9-96af-d95418680f08" />




## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/Ayodhya424/Image-Resizer-and-Converter.git
cd Image-Resizer-and-Converter
```


## Requirements.txt
```bash
flask
pillow
pillow-avif-plugin
```

## Usage
Run the Flask application:

```bash
python app.py
```

Once the server is running, open your browser and go to:
```bash
http://127.0.0.1:5000
```

# You will see
<img width="597" height="744" alt="image" src="https://github.com/user-attachments/assets/68c1e296-945c-4c6c-bdd2-0b1cc94d2b22" />

- Select a photo (PNG, JPEG, etc.)
- Enter desired width and height (max: 1920x1080)
- Enter target file size (max: 2000 KB)
- Click Upload and Resize
- Download the resized image.


## Author
Developed by **Ayodhay Kushwaha**  
GitHub: [Ayodhya424](https://github.com/Ayodhya424)

If you use this project or find it helpful, please give it a ⭐ on GitHub!





