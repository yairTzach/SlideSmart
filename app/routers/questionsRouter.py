# questionsRouter.py
from flask import Blueprint, request, render_template, current_app, redirect, url_for, session
import os
import re

questions_router = Blueprint('questions_router', __name__)

@questions_router.route('/questions/<filename>/<int:question_number>', methods=['GET', 'POST'])
@questions_router.route('/questions/<filename>/<int:question_number>', methods=['GET', 'POST'])
def questions(filename, question_number):
    # Initialize session variables for each level if not present
    if 'current_topic_score' not in session:
        session['current_topic_score'] = 0
        session['current_streak'] = 0
        session['current_level'] = 'easy'  # Levels: easy, medium, hard
        session['question_count'] = 0  # Total number of questions answered

    # Separate question counters for each difficulty level (do not reset across levels)
    if 'easy_question_number' not in session:
        session['easy_question_number'] = 1
    if 'medium_question_number' not in session:
        session['medium_question_number'] = 1
    if 'hard_question_number' not in session:
        session['hard_question_number'] = 1

    questions_folder = current_app.config['QUESTIONS_FOLDER']
    txt_filename = f"{filename}.txt"
    txt_path = os.path.join(questions_folder, txt_filename)

    if not os.path.exists(txt_path):
        return "Questions file not found", 404

    # Read and parse the questions
    with open(txt_path, 'r') as f:
        content = f.read()

    questions_data = parse_questions(content)

    # Flatten questions based on difficulty
    difficulty_levels = {'easy': [], 'medium': [], 'hard': []}
    for topic in questions_data:
        for question in topic['questions']:
            difficulty_levels[question['difficulty']].append(question)

    # Get the question number for the current difficulty level
    if session['current_level'] == 'easy':
        current_question_number = session['easy_question_number']
    elif session['current_level'] == 'medium':
        current_question_number = session['medium_question_number']
    else:
        current_question_number = session['hard_question_number']

    if request.method == 'POST':
        selected_option = request.form.get('option')
        current_question = difficulty_levels[session['current_level']][current_question_number - 1]

        # Check if answer is correct
        correct_answer = 'a'  # Assuming the correct answer is always 'a'
        if selected_option == correct_answer:
            # Increase score based on current difficulty
            if session['current_level'] == 'easy':
                session['current_topic_score'] += 10
                session['current_streak'] += 1
                if session['current_streak'] >= 1:
                    session['current_level'] = 'medium'  # Move to medium after 1 correct in easy
                    session['current_streak'] = 0
                print("Easy question correct, score is now:", session['current_topic_score'])

            elif session['current_level'] == 'medium':
                session['current_topic_score'] += 25
                session['current_streak'] += 1
                if session['current_streak'] >= 2:
                    session['current_level'] = 'hard'  # Move to hard after 2 correct in medium
                    session['current_streak'] = 0
                print("Medium question correct, score is now:", session['current_topic_score'])

            elif session['current_level'] == 'hard':
                session['current_topic_score'] += 40
                session['current_streak'] += 1
                print("Hard question correct, score is now:", session['current_topic_score'])
        else:
            # Reset streak and adjust difficulty if incorrect
            session['current_streak'] = 0
            if session['current_level'] == 'hard':
                session['current_level'] = 'medium'
            elif session['current_level'] == 'medium':
                session['current_level'] = 'easy'

        # Increment total question count (for all levels)
        session['question_count'] += 1

        # Check if the user won after 6 questions
        if session['question_count'] >= 6:
            if session['current_topic_score'] >= 75:
                return redirect(url_for('questions_router.results', filename=filename, result='won'))
            else:
                return redirect(url_for('questions_router.results', filename=filename, result='lost'))
        
        # Redirect to the next question without incrementing the question number yet
        return redirect(url_for('questions_router.questions', filename=filename, question_number=question_number + 1))

    # Render question page with current question and difficulty level
    current_question = difficulty_levels[session['current_level']][current_question_number - 1]
    
    # After rendering the question, increment the question counter for the correct level
    if session['current_level'] == 'easy':
        session_question_number = session['easy_question_number']
        session['easy_question_number'] += 1  # Increment only after rendering
    elif session['current_level'] == 'medium':
        session_question_number = session['medium_question_number']
        session['medium_question_number'] += 1  # Increment only after rendering
    else:
        session_question_number = session['hard_question_number']
        session['hard_question_number'] += 1  # Increment only after rendering

    return render_template(
        'questions.html',
        filename=filename,
        question_number=session_question_number,  # Use the session-based question number
        total_questions=6,  # Fixed or dynamically calculated number of questions
        question_data=current_question
    )

def parse_questions(content):
    import re

    topics = content.strip().split('---')
    parsed_topics = []

    for topic in topics:
        topic = topic.strip()
        if not topic:
            continue

        topic_lines = topic.split('\n')
        topic_title_line = topic_lines[0].strip()
        topic_title = re.sub(r'\*\*', '', topic_title_line).strip()

        # Initialize data structures
        questions = []
        current_difficulty = None

        i = 1  # Start from the second line
        while i < len(topic_lines):
            line = topic_lines[i].strip()

            # Check for difficulty level
            difficulty_match = re.match(r'\*\*(.*?)\*\*', line)
            if difficulty_match and 'Questions' in difficulty_match.group(1):
                current_difficulty = difficulty_match.group(1).replace('Questions:', '').strip().lower()  # Convert to lowercase
                i += 1
                continue

            # Check for question number
            question_match = re.match(r'(\d+)\.\s+(.*)', line)
            if question_match:
                question_text = question_match.group(2)
                options = []
                i += 1
                # Collect options
                while i < len(topic_lines):
                    option_line = topic_lines[i].strip()
                    option_match = re.match(r'(a|b|c|d)\)\s+(.*)', option_line)
                    if option_match:
                        options.append({'label': option_match.group(1), 'text': option_match.group(2)})
                        i += 1
                    else:
                        break
                # Append question
                questions.append({
                    'question': question_text,
                    'options': options,
                    'difficulty': current_difficulty
                })
            else:
                i += 1

        parsed_topics.append({
            'topic_title': topic_title,
            'questions': questions
        })

    return parsed_topics
