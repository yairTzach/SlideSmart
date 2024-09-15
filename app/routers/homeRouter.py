from flask import Blueprint, request, redirect, url_for, render_template, jsonify, current_app
import os
import time
from threading import Thread
from services.persist import process_pdf  # Import process_pdf from persist.py

home_router = Blueprint('home_router', __name__)

# Dictionary to hold processing status
processing_status = {}

@home_router.route('/')
def home():
    return render_template('home.html')

@home_router.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return 'No file part'
    
    file = request.files['pdfFile']
    if file.filename == '':
        return 'No selected file'
    
    if file and file.filename.endswith('.pdf'):
        filename = f"{int(time.time())}_{file.filename}"
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)
        
        # Set status as "processing" when upload happens
        processing_status[filename] = 'processing'

        # Start processing in a separate thread, pass config explicitly
        thread = Thread(target=process_pdf, args=(pdf_path, filename, current_app.config['QUESTIONS_FOLDER'], processing_status))
        thread.start()

        # Redirect to the waiting page with the filename in URL
        return redirect(url_for('home_router.wait', filename=filename))

    return 'Invalid file type'

@home_router.route('/wait/<filename>')
def wait(filename):
    # Render the wait.html page and pass the filename for polling
    return render_template('wait.html', filename=filename)

@home_router.route('/check_status/<filename>')
def check_status(filename):
    status = processing_status.get(filename, 'processing')  # Status is 'processing', 'complete', or 'failed'
    return jsonify({'status': status})
