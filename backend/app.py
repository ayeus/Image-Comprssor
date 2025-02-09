from flask import Flask, request, send_file, jsonify
from PIL import Image
import fitz  # PyMuPDF for PDF compression
import os

app = Flask(__name__)

# Ensure upload and compressed folders exist
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def compress_image(file_path, output_path, desired_size_kb):
    img = Image.open(file_path)
    quality = 95  # Start with high quality
    while quality >= 5:
        img.save(output_path, quality=quality)
        compressed_size_kb = os.path.getsize(output_path) / 1024
        if compressed_size_kb <= desired_size_kb:
            break
        quality -= 5  # Reduce quality incrementally

def compress_pdf(file_path, output_path, desired_size_kb):
    pdf = fitz.open(file_path)
    pdf.save(output_path, garbage=4, deflate=True)  # Compress PDF
    compressed_size_kb = os.path.getsize(output_path) / 1024
    if compressed_size_kb > desired_size_kb:
        raise Exception("PDF compression could not achieve the desired size.")

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    desired_size_kb = float(request.form.get('desired_size_kb', 10))  # Default: 1MB

    # Save the uploaded file
    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    # Determine file type and compress accordingly
    file_extension = os.path.splitext(file.filename)[1].lower()
    compressed_path = os.path.join(COMPRESSED_FOLDER, file.filename)

    try:
        if file_extension in ['.jpg', '.jpeg', '.png']:
            compress_image(upload_path, compressed_path, desired_size_kb)
        elif file_extension == '.pdf':
            compress_pdf(upload_path, compressed_path, desired_size_kb)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Return the compressed file
        return send_file(compressed_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)