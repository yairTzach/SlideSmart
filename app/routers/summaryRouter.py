# routers/summaryRouter.py

from flask import Blueprint, render_template, redirect, url_for, session

# Define the summary_router blueprint
summary_router = Blueprint('summary_router', __name__)

@summary_router.route('/questions/<filename>/summary', methods=['GET'])
@summary_router.route('/questions/<filename>/summary', methods=['GET'])
def summary(filename):
    if 'topics_scores' not in session or 'wrong_answers' not in session:
        return redirect(url_for('questions_router.questions', filename=filename, question_number=1))

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
        if topic not in wrong_answers_by_topic:
            wrong_answers_by_topic[topic] = []
        wrong_answers_by_topic[topic].append(wrong)

    # Clear session when the "Play Again" button is clicked
    session.clear()

    return render_template(
        'summary.html',
        topics_won=topics_won,
        topics_lost=topics_lost,
        wrong_answers=wrong_answers_by_topic,
        filename=filename
    )
