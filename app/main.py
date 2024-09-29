from flask import Flask
import os
from routers.homeRouter import home_router  # Relative import
from routers.loginRouter import login_router
from routers.registerRouter import register_router
from routers.questionsRouter import questions_router
from routers.aboutUsRouter import aboutUs_router
from routers.summaryRouter import summary_router
from routers.logoutRouter import logout_router
from routers.profileRouter import profile_router  # Import the new profile_router


from pymongo import MongoClient



main = Flask(__name__)
main.secret_key = os.urandom(24)
# Set up folders
UPLOAD_FOLDER = '../uploads'
QUESTIONS_FOLDER = '../generated_questions'
main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
main.config['QUESTIONS_FOLDER'] = QUESTIONS_FOLDER


# Create the folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QUESTIONS_FOLDER, exist_ok=True)

client = MongoClient('mongodb://localhost:27017/')
db = client['slideSmart_db']  
users_collection = db['users']  
main.config['db'] = db



# Register the blueprint after app is initialized
main.register_blueprint(home_router, url_prefix='/')
main.register_blueprint(login_router, url_prefix='/')
main.register_blueprint(register_router, url_prefix='/')
main.register_blueprint(aboutUs_router, url_prefix='/')
main.register_blueprint(questions_router, url_prefix='/')
main.register_blueprint(summary_router, url_prefix='/')
main.register_blueprint(logout_router, url_prefix='/')
main.register_blueprint(profile_router, url_prefix='/')  # Add this line




# Run the app
if __name__ == '__main__':
    main.run(debug=True)
