from flask import Blueprint, request, jsonify, redirect, url_for, render_template, current_app
from werkzeug.security import generate_password_hash

register_router = Blueprint('register_router', __name__)

@register_router.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        pdf = ""  # Empty for now

        users_collection = current_app.config['db']['users']

        # Double-check if username or email already exists
        existing_user = users_collection.find_one({
            '$or': [
                {'username': username},
                {'email': email}
            ]
        })

        if existing_user:
            if existing_user['username'] == username:
                return render_template('register.html', error="Username already exists")
            else:
                return render_template('register.html', error="Email already exists")

        # If the username and email are unique, hash the password and save the user
        hashed_password = generate_password_hash(password)

        try:
            result = users_collection.insert_one({
                'username': username,
                'email': email,
                'password': hashed_password,
                'pdf': pdf
            })
            if result.inserted_id:
                return redirect(url_for('login_router.login'))
            else:
                return render_template('register.html', error="Failed to register user")
        except Exception as e:
            print(f"Error inserting user: {e}")
            return render_template('register.html', error="An error occurred during registration")

    return render_template('register.html')

@register_router.route('/check_user_exists', methods=['POST'])
def check_user_exists():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging print to ensure data is received correctly
        
        username = data.get('username')
        email = data.get('email')
        
        # Check if the username or email exists in the database
        users_collection = current_app.config['db']['users']
        username_exists = users_collection.find_one({'username': username})
        email_exists = users_collection.find_one({'email': email})

        # Return the result in JSON format
        return jsonify({
            'usernameExists': bool(username_exists),
            'emailExists': bool(email_exists)
        })
    except Exception as e:
        print(f"Error in check_user_exists: {e}")  # Print error for debugging
        return jsonify({'error': 'Server encountered an error'}), 500