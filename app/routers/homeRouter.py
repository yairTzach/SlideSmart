from flask import Blueprint, request, redirect, url_for, render_template, jsonify, current_app
import os
import time
from threading import Thread
from services.persist import process_pdf  # Import process_pdf from persist.py
from bson import ObjectId

home_router = Blueprint('home_router', __name__)

# Dictionary to hold processing status
processing_status = {}

@home_router.route('/home')
def home():
    user_id = request.cookies.get('userId')  # Get userId from cookies
    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            # Convert user_id to ObjectId and check if the user exists in the database
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            if user:
                return render_template('home.html')
            else:
                # Handle the case where the userId does not exist in the database
                return redirect(url_for('login_router.login'))
        except Exception as e:
            # Handle cases where ObjectId conversion fails or other exceptions
            print(f"Error checking user ID: {e}")
            return redirect(url_for('login_router.login'))
    else:
        # Redirect to login if no userId cookie is found
        return redirect(url_for('login_router.login'))


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
    user_id = request.cookies.get('userId')  # Get userId from cookies
    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            # Convert user_id to ObjectId and check if the user exists in the database
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            if user:
                    return render_template('wait.html', filename=filename)
            else:
                # Handle the case where the userId does not exist in the database
                return redirect(url_for('login_router.login'))
        except Exception as e:
            # Handle cases where ObjectId conversion fails or other exceptions
            print(f"Error checking user ID: {e}")
            return redirect(url_for('login_router.login'))
    else:
        # Redirect to login if no userId cookie is found
        return redirect(url_for('login_router.login'))
    # Render the wait.html page and pass the filename for polling

@home_router.route('/check_status/<filename>')
def check_status(filename):
    status = processing_status.get(filename, 'processing')  # Status is 'processing', 'complete', or 'failed'
    return jsonify({'status': status})
# homeRouter.py

from flask import Blueprint, request, redirect, url_for, render_template, jsonify, current_app, session  # Added 'session' import

# ... rest of your imports ...

@home_router.route('/chooseGame/<filename>')
def choose_game(filename):
    session_keys = [
    'current_topic_score', 'current_streak', 'current_level',
    'question_count', 'current_topic_index', 'topics_scores',
    'wrong_answers', 'total_questions_answered',
    'easy_question_number', 'medium_question_number',
    'hard_question_number'
    ]
    for key in session_keys:
        session.pop(key, None)

    user_id = request.cookies.get('userId')
    print(f"[DEBUG] User ID from cookie in choose_game: {user_id}")  # Debugging

    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            # Verify if the user exists in the database
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            print(f"[DEBUG] User document in choose_game: {user}")  # Debugging

            if user:
                # Build the choose game URL
                choose_game_url = url_for('home_router.choose_game', filename=filename)
                print(f"[DEBUG] choose_game_url to be stored: {choose_game_url}")  # Debugging

                # Update the user's document with the choose_game_url
                result = users_collection.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$set': {'choose_game_url': choose_game_url}}
                )
                print(f"[DEBUG] Update result: {result.modified_count} document(s) updated.")  # Debugging

                return render_template('chooseGame.html', filename=filename)
            else:
                print("[DEBUG] No user found with given user ID in choose_game.")  # Debugging
                return redirect(url_for('login_router.login'))
        except Exception as e:
            print(f"[ERROR] Exception in choose_game: {e}")  # Debugging
            return redirect(url_for('login_router.login'))
    else:
        print("[DEBUG] No user ID found in cookies in choose_game.")  # Debugging
        return redirect(url_for('login_router.login'))
