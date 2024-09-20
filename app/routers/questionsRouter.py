# questionsRouter.py
from flask import Blueprint, request, render_template, current_app, redirect, url_for, session
import os
import re

questions_router = Blueprint('questions_router', __name__)

@questions_router.route('/questions/<filename>/<int:question_number>', methods=['GET', 'POST'])
def questions(filename, question_number):
    questions_folder = current_app.config['QUESTIONS_FOLDER']
    txt_filename = f"{filename}.txt"
    txt_path = os.path.join(questions_folder, txt_filename)
    if not os.path.exists(txt_path):
        return "Questions file not found", 404

    # Read and parse the questions
    with open(txt_path, 'r') as f:
        content = f.read()

    questions_data = parse_questions(content)

    # Flatten all questions into a single list for easy indexing
    all_questions = []
    for topic_index, topic in enumerate(questions_data):
        for question_index, question in enumerate(topic['questions']):
            all_questions.append({
                'topic_index': topic_index,
                'question_index': question_index,
                'topic_title': topic['topic_title'],
                'question': question
            })

    total_questions = len(all_questions)

    if request.method == 'POST':
        # Handle form submission
        selected_option = request.form.get('option')
        # Store the answer in the session
        user_answers = session.get('user_answers', {})
        current_question = all_questions[question_number - 1]
        key = f"{current_question['topic_index']}_{current_question['question_index']}"
        user_answers[key] = selected_option
        session['user_answers'] = user_answers

        if 'next' in request.form:
            if question_number < total_questions:
                return redirect(url_for('questions_router.questions', filename=filename, question_number=question_number + 1))
            else:
                # End of questions, show results
                return redirect(url_for('questions_router.results', filename=filename))
        elif 'previous' in request.form:
            if question_number > 1:
                return redirect(url_for('questions_router.questions', filename=filename, question_number=question_number - 1))
            else:
                # Already at the first question
                return redirect(url_for('questions_router.questions', filename=filename, question_number=1))

    else:
        # GET request
        if question_number < 1 or question_number > total_questions:
            return "Invalid question number", 404

        current_question = all_questions[question_number - 1]
        # Retrieve user's previous answer if any
        user_answers = session.get('user_answers', {})
        key = f"{current_question['topic_index']}_{current_question['question_index']}"
        selected_option = user_answers.get(key, None)

        return render_template(
            'questions.html',
            filename=filename,
            question_number=question_number,
            total_questions=total_questions,
            question_data=current_question,
            selected_option=selected_option
        )

@questions_router.route('/results/<filename>')
def results(filename):
    # Load questions data as before
    questions_folder = current_app.config['QUESTIONS_FOLDER']
    txt_filename = f"{filename}.txt"
    txt_path = os.path.join(questions_folder, txt_filename)
    if not os.path.exists(txt_path):
        return "Questions file not found", 404

    # Read and parse the questions
    with open(txt_path, 'r') as f:
        content = f.read()

    questions_data = parse_questions(content)

    # Flatten all questions into a single list for easy indexing
    all_questions = []
    for topic_index, topic in enumerate(questions_data):
        for question_index, question in enumerate(topic['questions']):
            all_questions.append({
                'topic_index': topic_index,
                'question_index': question_index,
                'topic_title': topic['topic_title'],
                'question': question
            })

    total_questions = len(all_questions)
    correct_answers = 0
    user_answers = session.get('user_answers', {})

    for item in all_questions:
        key = f"{item['topic_index']}_{item['question_index']}"
        user_answer = user_answers.get(key, '')
        # Correct answer is always 'a' as per the prompt
        if user_answer == 'a':
            correct_answers += 1

    # Clear user answers from session
    session.pop('user_answers', None)

    return render_template('results.html', total_questions=total_questions, correct_answers=correct_answers)

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
                current_difficulty = difficulty_match.group(1).replace('Questions:', '').strip()
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
