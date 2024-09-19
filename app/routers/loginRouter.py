# routers/loginRouter.py

from flask import Blueprint, request, render_template, jsonify, current_app, make_response
from werkzeug.security import check_password_hash

login_router = Blueprint('login_router', __name__)

@login_router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get JSON data from request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({'success': False, 'message': 'Missing username or password'}), 400

        # Access the database
        db = current_app.config['db']
        users_collection = db['users']

        # Find the user
        user = users_collection.find_one({'username': username})

        if user:
            stored_hashed_password = user.get('password')  # This is a string

            # Check the password using Werkzeug's check_password_hash
            if check_password_hash(stored_hashed_password, password):
                # Successful login
                # Set cookies
                response = make_response(jsonify({'success': True}))
                response.set_cookie('userId', str(user['_id']), httponly=True)
                response.set_cookie('username', user['username'], httponly=True)
                return response
            else:
                # Invalid password
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
        else:
            # User not found
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    else:
        # GET request, render login page
        return render_template('login.html')
