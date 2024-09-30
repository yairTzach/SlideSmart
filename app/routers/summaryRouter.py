# routers/summaryRouter.py

from flask import Blueprint, render_template, redirect, url_for, session, current_app, request
from bson import ObjectId

summary_router = Blueprint('summary_router', __name__)

@summary_router.route('/questions/<filename>/summary', methods=['GET'])
def summary(filename):
    user_id = request.cookies.get('userId')
    if not user_id:
        return redirect(url_for('login_router.login'))

    db = current_app.config['db']
    users_collection = db['users']

    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return redirect(url_for('login_router.login'))
    except Exception as e:
        print(f"Error fetching user: {e}")
        return redirect(url_for('login_router.login'))

    # Check if required session variables are missing and display an appropriate message
    if 'topics_scores' not in session or 'wrong_answers' not in session:
        return render_template('summary_error.html', message="Your session has expired. Please start a new game.")

    topics_won = []
    topics_lost = []

    # Define the passing score
    PASSING_SCORE = 75

    for topic in session['topics_scores']:
        if topic['score'] >= PASSING_SCORE:
            topics_won.append(topic)
        else:
            topics_lost.append(topic)

    # Organize wrong answers by topic
    wrong_answers_by_topic = {}
    for wrong in session['wrong_answers']:
        topic = wrong['topic_name']
        wrong_answers_by_topic.setdefault(topic, []).append(wrong)

    # Retrieve choose_game_url from the user's document in MongoDB
    user_id = request.cookies.get('userId')

    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            choose_game_url = user.get('choose_game_url', url_for('home_router.home')) if user else url_for('home_router.home')
        except Exception as e:
            print(f"[ERROR] Exception while retrieving user: {e}")
            choose_game_url = url_for('home_router.home')
    else:
        choose_game_url = url_for('home_router.home')

    return render_template('summary.html',
                           topics_won=topics_won,
                           topics_lost=topics_lost,
                           wrong_answers=wrong_answers_by_topic,
                           filename=filename,
                           choose_game_url=choose_game_url,
                           game_mode='Standard',
                           passing_score=PASSING_SCORE)

# Similar changes can be made to `hard_summary`, `medium_summary`, and `easy_summary` routes as well.

@summary_router.route('/hard_questions/<filename>/summary', methods=['GET'])
def hard_summary(filename):
    # Check required session variables for hard mode
    if 'hard_topics_scores' not in session or 'hard_wrong_answers' not in session:
        return redirect(url_for('hard_questions_router.hard_questions',
                                filename=filename, question_number=1))

    topics_won = []
    topics_lost = []

    # Define passing score for hard mode
    PASSING_SCORE = 80  # Adjust as needed

    for topic in session['hard_topics_scores']:
        if topic['score'] >= PASSING_SCORE:
            topics_won.append(topic)
        else:
            topics_lost.append(topic)

    # Organize wrong answers by topic
    wrong_answers_by_topic = {}
    for wrong in session['hard_wrong_answers']:
        topic = wrong['topic_name']
        wrong_answers_by_topic.setdefault(topic, []).append(wrong)

    # Clear hard game-related session variables
    session_keys = [
        'hard_current_topic_score', 'hard_question_count',
        'hard_current_topic_index', 'hard_topics_scores',
        'hard_wrong_answers'
    ]
    for key in session_keys:
        session.pop(key, None)

    # Retrieve choose_game_url from the user's document in MongoDB
    user_id = request.cookies.get('userId')
    print(f"[DEBUG] User ID from cookie: {user_id}")  # Debugging

    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            print(f"[DEBUG] User document retrieved: {user}")  # Debugging

            if user:
                choose_game_url = user.get('choose_game_url', url_for('home_router.home'))
                print(f"[DEBUG] choose_game_url retrieved from MongoDB: {choose_game_url}")  # Debugging
            else:
                print("[DEBUG] No user found with given user ID.")  # Debugging
                choose_game_url = url_for('home_router.home')
        except Exception as e:
            print(f"[ERROR] Exception while retrieving user: {e}")  # Debugging
            choose_game_url = url_for('home_router.home')
    else:
        print("[DEBUG] No user ID found in cookies.")  # Debugging
        choose_game_url = url_for('home_router.home')

    return render_template('summary.html',
                           topics_won=topics_won,
                           topics_lost=topics_lost,
                           wrong_answers=wrong_answers_by_topic,
                           filename=filename,
                           choose_game_url=choose_game_url,
                           game_mode='Hard',
                           passing_score=PASSING_SCORE)
@summary_router.route('/medium_questions/<filename>/summary', methods=['GET'])
def medium_summary(filename):
    # Check required session variables for medium mode
    if 'medium_topics_scores' not in session or 'medium_wrong_answers' not in session:
        return redirect(url_for('medium_questions_router.medium_questions',
                                filename=filename, question_number=1))

    topics_won = []
    topics_lost = []

    # Define passing score for medium mode
    PASSING_SCORE = 80  # Adjust as needed

    for topic in session['medium_topics_scores']:
        if topic['score'] >= PASSING_SCORE:
            topics_won.append(topic)
        else:
            topics_lost.append(topic)

    # Organize wrong answers by topic
    wrong_answers_by_topic = {}
    for wrong in session['medium_wrong_answers']:
        topic = wrong['topic_name']
        wrong_answers_by_topic.setdefault(topic, []).append(wrong)

    # Clear medium game-related session variables
    session_keys = [
        'medium_current_topic_score', 'medium_question_count',
        'medium_current_topic_index', 'medium_topics_scores',
        'medium_wrong_answers'
    ]
    for key in session_keys:
        session.pop(key, None)

    # Retrieve choose_game_url from the user's document in MongoDB
    user_id = request.cookies.get('userId')
    print(f"[DEBUG] User ID from cookie: {user_id}")  # Debugging

    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            print(f"[DEBUG] User document retrieved: {user}")  # Debugging

            if user:
                choose_game_url = user.get('choose_game_url', url_for('home_router.home'))
                print(f"[DEBUG] choose_game_url retrieved from MongoDB: {choose_game_url}")  # Debugging
            else:
                print("[DEBUG] No user found with given user ID.")  # Debugging
                choose_game_url = url_for('home_router.home')
        except Exception as e:
            print(f"[ERROR] Exception while retrieving user: {e}")  # Debugging
            choose_game_url = url_for('home_router.home')
    else:
        print("[DEBUG] No user ID found in cookies.")  # Debugging
        choose_game_url = url_for('home_router.home')

    return render_template('summary.html',
                           topics_won=topics_won,
                           topics_lost=topics_lost,
                           wrong_answers=wrong_answers_by_topic,
                           filename=filename,
                           choose_game_url=choose_game_url,
                           game_mode='Medium',
                           passing_score=PASSING_SCORE)

@summary_router.route('/easy_questions/<filename>/summary', methods=['GET'])
def easy_summary(filename):
    # Check required session variables for easy mode
    if 'easy_topics_scores' not in session or 'easy_wrong_answers' not in session:
        return redirect(url_for('easy_questions_router.easy_questions',
                                filename=filename, question_number=1))

    topics_won = []
    topics_lost = []

    # Define passing score for easy mode
    PASSING_SCORE = 80  # Adjust as needed

    for topic in session['easy_topics_scores']:
        if topic['score'] >= PASSING_SCORE:
            topics_won.append(topic)
        else:
            topics_lost.append(topic)

    # Organize wrong answers by topic
    wrong_answers_by_topic = {}
    for wrong in session['easy_wrong_answers']:
        topic = wrong['topic_name']
        wrong_answers_by_topic.setdefault(topic, []).append(wrong)

    # Clear easy game-related session variables

    # Retrieve choose_game_url from the user's document in MongoDB
    user_id = request.cookies.get('userId')
    print(f"[DEBUG] User ID from cookie: {user_id}")  # Debugging

    if user_id:
        db = current_app.config['db']
        users_collection = db['users']
        try:
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            print(f"[DEBUG] User document retrieved: {user}")  # Debugging

            if user:
                choose_game_url = user.get('choose_game_url', url_for('home_router.home'))
                print(f"[DEBUG] choose_game_url retrieved from MongoDB: {choose_game_url}")  # Debugging
            else:
                print("[DEBUG] No user found with given user ID.")  # Debugging
                choose_game_url = url_for('home_router.home')
        except Exception as e:
            print(f"[ERROR] Exception while retrieving user: {e}")  # Debugging
            choose_game_url = url_for('home_router.home')
    else:
        print("[DEBUG] No user ID found in cookies.")  # Debugging
        choose_game_url = url_for('home_router.home')

    return render_template('summary.html',
                           topics_won=topics_won,
                           topics_lost=topics_lost,
                           wrong_answers=wrong_answers_by_topic,
                           filename=filename,
                           choose_game_url=choose_game_url,
                           game_mode='Easy',
                           passing_score=PASSING_SCORE)
