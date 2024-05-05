# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

# Initialize the Flask application
application = Flask(__name__)

# List to store user feedback temporarily
user_feedbacks = []

# Home page route
@application.route('/')
def home():
    return render_template('index.html')

# Survey page route
@application.route('/survey')
def survey_page():
    return render_template('survey.html')

# Route to handle feedback submission
@application.route('/submit_feedback', methods=['POST'])
def handle_feedback():
    feedback_category = request.form.get('category')
    user_name = request.form.get('name')
    user_feedback = request.form.get('feedback')
    positive_points = int(request.form.get('liked'))
    negative_points = int(request.form.get('disliked'))
    user_feedbacks.append({
        'category': feedback_category,
        'name': user_name,
        'feedback': user_feedback,
        'liked': positive_points,
        'disliked': negative_points
    })
    return redirect(url_for('home'))

# Route to display feedback comparisons
@application.route('/comparison')
def show_comparison():
    feedback_distribution = {'Student': [], 'Parent': [], 'Teacher': [], 'Online Class': [], 'Normal Class': []}
    for feedback in user_feedbacks:
        if feedback['category'] in feedback_distribution:
            feedback_distribution[feedback['category']].append(feedback)
        else:
            print(f"Unrecognized category: {feedback['category']}")
    return render_template('comparison.html', category_map=feedback_distribution)

# Route for feedback analysis
@application.route('/analysis')
def feedback_analysis():
    categories = ['Student', 'Parent', 'Teacher', 'Online Class', 'Normal Class']
    positives = [0] * len(categories)
    negatives = [0] * len(categories)

    for feedback in user_feedbacks:
        category_index = categories.index(feedback['category'])
        positives[category_index] += feedback['liked']
        negatives[category_index] += feedback['disliked']

    json_positives = json.dumps(positives)
    json_negatives = json.dumps(negatives)

    return render_template('analysis.html', liked_data=json_positives, disliked_data=json_negatives)

# Start the Flask application
if __name__ == '__main__':
    application.run(debug=True)
