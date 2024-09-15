from flask import Flask
import os
from routers.homeRouter import home_router  # Relative import

main = Flask(__name__)

# Set up folders
UPLOAD_FOLDER = '../uploads'
QUESTIONS_FOLDER = '../generated_questions'
main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
main.config['QUESTIONS_FOLDER'] = QUESTIONS_FOLDER

# Create the folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QUESTIONS_FOLDER, exist_ok=True)

# Register the blueprint after app is initialized
main.register_blueprint(home_router, url_prefix='/')

# Run the app
if __name__ == '__main__':
    main.run(debug=True)
