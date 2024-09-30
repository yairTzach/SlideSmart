# routers/mediumQuestionsRouter.py

from flask import Blueprint, request, render_template, current_app, redirect, url_for, session
import os
import random

medium_questions_router = Blueprint('medium_questions_router', __name__)

@medium_questions_router.route('/medium_questions/<filename>/<int:question_number>', methods=['GET', 'POST'])
def medium_questions(filename, question_number):
    # Initialize session variables specific to medium mode
    if 'medium_current_topic_score' not in session:
        session['medium_current_topic_score'] = 0
        session['medium_question_count'] = 0
        session['medium_current_topic_index'] = 0
        session['medium_topics_scores'] = []
        session['medium_wrong_answers'] = []

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
    current_topic_index = session.get('medium_current_topic_index', 0)
    if current_topic_index >= len(questions_data):
        return redirect(url_for('summary_router.medium_summary', filename=filename))

    current_topic = questions_data[current_topic_index]
    current_topic_name = current_topic['topic_title']

    # Determine if the current topic is the last one
    is_last_topic = (current_topic_index == len(questions_data) - 1)

    # Filter medium questions
    medium_questions = [q for q in current_topic['questions'] if q['difficulty'] == 'medium']

    if request.method == 'POST':
        # Get selected option and correct answer from the form
        selected_option = request.form.get('option')
        correct_answer = request.form.get('correct_answer')  # Value from hidden input field

        try:
            current_question = medium_questions[question_number - 1]
        except IndexError:
            return "Question not found", 404

        # Compare the user's selected option with the correct answer
        if selected_option == correct_answer:
            session['medium_current_topic_score'] += 30  # Medium questions are worth 30 points
        else:
            if session['medium_current_topic_score'] >= 5:
                session['medium_current_topic_score'] -= 10

            # Record the wrong answer details, including options
            wrong_answer_detail = {
                'topic_name': current_topic_name,
                'question': current_question['question'],
                'options': current_question['options'],
                'correct_answer': correct_answer,
                'selected_option': selected_option
            }
            session['medium_wrong_answers'].append(wrong_answer_detail)

        # Increment question counts
        session['medium_question_count'] += 1

        # Check if 6 questions have been answered in this topic
        if session['medium_question_count'] >= 6 or question_number >= len(medium_questions):
            session['medium_topics_scores'].append({
                'topic_name': current_topic_name,
                'score': session['medium_current_topic_score']
            })

            session['medium_current_topic_index'] += 1
            session['medium_question_count'] = 0
            session['medium_current_topic_score'] = 0

            if session['medium_current_topic_index'] >= total_topics:
                return redirect(url_for('summary_router.medium_summary', filename=filename))

            return redirect(url_for('medium_questions_router.medium_questions', filename=filename, question_number=1))

        return redirect(url_for('medium_questions_router.medium_questions', filename=filename, question_number=question_number + 1))

    # Handle GET request: Render the current question
    try:
        current_question = medium_questions[question_number - 1]
    except IndexError:
        return redirect(url_for('summary_router.medium_summary', filename=filename))

    # Save the correct answer before shuffling the options
    correct_answer = current_question['options'][0]['text']

    # Shuffle the options before rendering
    options = current_question['options']
    random.shuffle(options)
    current_question['options'] = options

    return render_template(
        'medium_questions.html',  # Use the same template as hard mode if appropriate
        filename=filename,
        question_number=question_number,
        total_questions=6,
        question_data=current_question,
        correct_answer=correct_answer,  # Pass correct answer to the template
        topic_name=current_topic_name,
        topic_score=session['medium_current_topic_score'],
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
