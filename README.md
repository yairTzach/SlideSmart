Slide Smart
URL: http://127.0.0.1:5000

Project Overview
Slide Smart is an interactive educational platform designed to make learning more accessible and adaptive for users of all ages. This platform dynamically generates quizzes based on user-uploaded PDF content, leveraging tools such as Python, Flask, and the OpenAI API. Slide Smart adjusts quiz difficulty in real-time based on user performance, providing a unique learning experience tailored to each user. With scoring, feedback, multiple game modes, and robust session management, Slide Smart enhances engagement and educational outcomes.

Key Features
Adaptive Quiz Algorithm: Custom-built algorithm that dynamically adjusts quiz difficulty based on user performance, offering more challenging questions as users answer correctly.
Dynamic PDF Text Extraction & Question Generation: Automatically extracts text from uploaded PDFs to generate relevant quiz questions.
Game Modes: Offers distinct levels such as Easy, Medium, and Hard, allowing users to select their preferred challenge.
Detailed Feedback Page: Provides performance insights, including strengths, areas for improvement, incorrect answers, and correct answers.
User Authentication & Profile Management: Allows users to sign up, log in, and manage their profile information for a personalized experience.
Project Structure
php
Copy code
SlideSmart/
├── README.md                      # Project documentation
├── app/                           # Main application folder
│   ├── main.py                    # Entry point for the application
│   ├── routers/                   # Route handlers
│   │   ├── aboutUsRouter.py
│   │   ├── easyQuestionsRouter.py
│   │   ├── hardQuestionsRouter.py
│   │   ├── homeRouter.py
│   │   ├── loginRouter.py
│   │   ├── logoutRouter.py
│   │   ├── mediumQuestionsRouter.py
│   │   ├── profileRouter.py
│   │   ├── questionsRouter.py
│   │   ├── registerRouter.py
│   │   └── summaryRouter.py
│   ├── services/                  # Utility and persistence services
│   │   └── persist.py             # Data persistence utility
│   ├── static/                    # Static files (CSS, images, JavaScript, sound)
│   │   ├── css/                   # CSS stylesheets
│   │   │   ├── aboutUs.css
│   │   │   ├── chooseGame.css
│   │   │   ├── home.css
│   │   │   ├── login.css
│   │   │   ├── navbar.css
│   │   │   ├── nicepage.css
│   │   │   ├── profile.css
│   │   │   ├── questions.css
│   │   │   ├── register.css
│   │   │   ├── summary.css
│   │   │   └── wait.css
│   │   ├── images/                # Image assets
│   │   │   └── [image files]
│   │   ├── js/                    # JavaScript files
│   │   │   ├── jquery.js
│   │   │   ├── login.js
│   │   │   ├── register.js
│   │   │   ├── utils.js
│   │   │   └── wait.js
│   │   └── sound/                 # Sound assets
│   │       ├── background.mp3
│   │       └── questions.mp3
│   └── templates/                 # HTML templates
│       ├── aboutUs.html
│       ├── audioPlayer.html
│       ├── base.html
│       ├── chooseGame.html
│       ├── easy_questions.html
│       ├── hard_questions.html
│       ├── home.html
│       ├── login.html
│       ├── medium_questions.html
│       ├── profile.html
│       ├── questions.html
│       ├── register.html
│       ├── summary.html
│       └── wait.html
├── generated_questions/           # Stores generated questions
└── uploads/                       # Stores uploaded files
Installation & Setup
Prerequisites
Python 3.7+: Ensure Python is installed.
MongoDB: Install MongoDB for user data storage and quiz progress tracking.
Step 1: Project Setup
Download and Extract the project zip file to your computer.

Open the Terminal and navigate to the project directory:

bash
Copy code
cd /path/to/SlideSmart
Step 2: Install Dependencies
Install all necessary dependencies using the following command:

bash
Copy code
pip install -r requirements.txt
Step 3: Configure Environment Variables
Create a .env file in the root directory with your MongoDB URI and other environment variables:

env
Copy code
MONGODB_URI=mongodb://localhost:27017/slide_smart
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
Replace your_secret_key and your_openai_api_key with your actual secret key and OpenAI API key.

Step 4: Start the Application
Launch the application using the following command:

bash
Copy code
python app/main.py
The app should now be accessible at http://127.0.0.1:5000.



