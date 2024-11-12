from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from encryption.encryption_utils import encrypt_image, verify_encrypted_file
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session and flash messages
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' in request.files and 'encryption_key' in request.form:
            # Encrypt image
            image = request.files['image']
            encryption_key = request.form['encryption_key']
            encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_image.bin')
            encrypt_image(image, encryption_key, encrypted_path)
            flash('Image encrypted successfully!', 'success')
            return render_template('index.html', encrypted=True)
        
        elif 'encrypted_file' in request.files and 'decryption_key' in request.form:
            # Decrypt image if the key and file are correct
            encrypted_file = request.files['encrypted_file']
            decryption_key = request.form['decryption_key']
            decrypted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted_image.png')
            is_verified = verify_encrypted_file(encrypted_file, decryption_key, decrypted_image_path)
            if is_verified:
                return send_file(decrypted_image_path, mimetype='image/png')
            else:
                flash('Decryption failed. Incorrect key or file.', 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)