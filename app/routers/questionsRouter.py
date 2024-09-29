# routers/questionsRouter.py

from flask import Blueprint, request, render_template, current_app, redirect, url_for, session
import os
import re
import random  # Moved import to the top for better practice

questions_router = Blueprint('questions_router', __name__)

@questions_router.route('/questions/<filename>/<int:question_number>', methods=['GET', 'POST'])
def questions(filename, question_number):
    # Initialize session variables if not present
    if 'current_topic_score' not in session:
        session['current_topic_score'] = 0
        session['current_streak'] = 0
        session['current_level'] = 'easy'
        session['question_count'] = 0
        session['current_topic_index'] = 0
        session['topics_scores'] = []
        session['wrong_answers'] = []
        session['total_questions_answered'] = 0

    # Initialize difficulty level question counters
    if 'easy_question_number' not in session:
        session['easy_question_number'] = 1
    if 'medium_question_number' not in session:
        session['medium_question_number'] = 1
    if 'hard_question_number' not in session:
        session['hard_question_number'] = 1

    # Read and parse the questions
    questions_folder = current_app.config['QUESTIONS_FOLDER']
    txt_filename = f"{filename}.txt"
    txt_path = os.path.join(questions_folder, txt_filename)

    if not os.path.exists(txt_path):
        return "Questions file not found", 404

    with open(txt_path, 'r') as f:
        content = f.read()

    questions_data = parse_questions(content)
    total_topics = len(questions_data)  # Total number of topics

    # Get the current topic based on session
    current_topic_index = session.get('current_topic_index', 0)
    if current_topic_index >= len(questions_data):
        return redirect(url_for('summary_router.summary', filename=filename))

    current_topic = questions_data[current_topic_index]
    current_topic_name = current_topic['topic_title']

    # Determine if the current topic is the last one
    is_last_topic = (current_topic_index == len(questions_data) - 1)

    # Flatten questions based on difficulty
    difficulty_levels = {'easy': [], 'medium': [], 'hard': []}
    for question in current_topic['questions']:
        difficulty_levels[question['difficulty']].append(question)

    current_level = session['current_level']
    if current_level == 'easy':
        current_question_number = session['easy_question_number']
    elif current_level == 'medium':
        current_question_number = session['medium_question_number']
    else:
        current_question_number = session['hard_question_number']

    if request.method == 'POST':
        # Get selected option and correct answer from the form
        selected_option = request.form.get('option')
        correct_answer = request.form.get('correct_answer')  # Value from hidden input field

        try:
            current_question = difficulty_levels[current_level][current_question_number - 1]
        except IndexError:
            return "Question not found", 404

        # Capture the level being answered before any changes
        previous_level = current_level

        # Compare the user's selected option with the correct answer
        if selected_option == correct_answer:
            session['current_topic_score'] += get_score_increment(previous_level)
            session['current_streak'] += 1
            session['current_level'], session['current_streak'] = update_level(previous_level, session['current_streak'])
        else:
            if  session['current_topic_score'] >= 5:
                session['current_topic_score'] += -5

            # Record the wrong answer details
            wrong_answer_detail = {
                'topic_name': current_topic_name,
                'question': current_question['question'],
                'options': current_question['options'],
                'correct_answer': correct_answer,
                'selected_option': selected_option
            }
            session['wrong_answers'].append(wrong_answer_detail)

            # Reset streak and demote level
            session['current_streak'] = 0
            session['current_level'] = demote_level(previous_level)

        # Increment total question counts
        session['question_count'] += 1
        session['total_questions_answered'] += 1

        # Increment the question number for the level that was just answered
        if previous_level == 'easy':
            session['easy_question_number'] += 1
        elif previous_level == 'medium':
            session['medium_question_number'] += 1
        else:
            session['hard_question_number'] += 1

        # Check if 6 questions have been answered in this topic
        if session['question_count'] >= 6:
            session['topics_scores'].append({
                'topic_name': current_topic_name,
                'score': session['current_topic_score']
            })

            session['current_topic_index'] += 1
            session['current_level'] = 'easy'
            session['question_count'] = 0
            session['easy_question_number'] = 1
            session['medium_question_number'] = 1
            session['hard_question_number'] = 1
            session['current_topic_score'] = 0

            if session['current_topic_index'] >= total_topics:
                return redirect(url_for('summary_router.summary', filename=filename))

            return redirect(url_for('questions_router.questions', filename=filename, question_number=1))

        # Check if total questions answered have reached 30
        if session['total_questions_answered'] >= 30:
            session['topics_scores'].append({
                'topic_name': current_topic_name,
                'score': session['current_topic_score']
            })
            return redirect(url_for('summary_router.summary', filename=filename))

        return redirect(url_for('questions_router.questions', filename=filename, question_number=question_number + 1))

    # Handle GET request: Render the current question without modifying session counters
    try:
        current_question = difficulty_levels[current_level][current_question_number - 1]
    except IndexError:
        return "Question not found", 404

    # Save the correct answer before shuffling the options
    correct_answer = current_question['options'][0]['text']

    # Shuffle the options before rendering
    options = current_question['options']
    random.shuffle(options)

    return render_template(
        'questions.html',
        filename=filename,
        question_number=question_number,
        total_questions=6,
        question_data=current_question,
        correct_answer=correct_answer,  # Pass correct answer to the template
        topic_name=current_topic_name,
        topic_score=session['current_topic_score'],
        is_last_topic=is_last_topic,  # Pass the flag to the template
        total_topics=total_topics,
        current_topic_index=current_topic_index + 1  # 1-based index for display
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


def get_score_increment(level):
    """Returns the score increment based on the difficulty level."""
    score_map = {
        'easy': 10,
        'medium': 25,
        'hard': 40
    }
    return score_map.get(level, 0)


def update_level(current_level, streak):
    """
    Updates the difficulty level based on the current level and streak.
    Returns a tuple of (new_level, reset_streak).
    """
    if current_level == 'easy':
        if streak >= 1:
            return ('medium', 0)
    elif current_level == 'medium':
        if streak >= 2:
            return ('hard', 0)
    elif current_level == 'hard':
        # You might want to define behavior for streaks in 'hard' level
        pass
    return (current_level, streak)


def demote_level(current_level):
    """
    Demotes the difficulty level based on the current level.
    Returns the new_level.
    """
    if current_level == 'hard':
        return 'medium'
    elif current_level == 'medium':
        return 'easy'
    return 'easy'
