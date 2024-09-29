from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, make_response
from bson import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

profile_router = Blueprint('profile_router', __name__)

@profile_router.route('/profile', methods=['GET'])
def profile():
    # Get user ID from cookies
    user_id = request.cookies.get('userId')
    if not user_id:
        return redirect(url_for('login_router.login'))

    db = current_app.config['db']
    users_collection = db['users']

    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return redirect(url_for('login_router.login'))
    except Exception as e:
        print(f"Error fetching user: {e}")
        return redirect(url_for('login_router.login'))

    return render_template('profile.html', user=user)

@profile_router.route('/update-details', methods=['POST'])
def update_details():
    user_id = request.cookies.get('userId')
    if not user_id:
        return redirect(url_for('login_router.login'))

    db = current_app.config['db']
    users_collection = db['users']

    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return redirect(url_for('login_router.login'))
    except Exception as e:
        print(f"Error fetching user: {e}")
        return redirect(url_for('login_router.login'))

    new_username = request.form.get('username')
    new_email = request.form.get('email')

    update_fields = {}

    if new_username != user.get('username'):
        existing_user = users_collection.find_one({'username': new_username})
        if existing_user and existing_user['_id'] != user['_id']:
            flash('Username is already taken.', 'error')
            return redirect(url_for('profile_router.profile'))
        update_fields['username'] = new_username

    if new_email != user.get('email'):
        existing_user = users_collection.find_one({'email': new_email})
        if existing_user and existing_user['_id'] != user['_id']:
            flash('Email is already registered.', 'error')
            return redirect(url_for('profile_router.profile'))
        update_fields['email'] = new_email

    if update_fields:
        users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_fields}
        )
        flash('Details updated successfully.', 'success')
    else:
        flash('No changes made.', 'error')

    return redirect(url_for('profile_router.profile'))

@profile_router.route('/change-password', methods=['POST'])
def change_password():
    user_id = request.cookies.get('userId')
    if not user_id:
        return redirect(url_for('login_router.login'))

    db = current_app.config['db']
    users_collection = db['users']

    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return redirect(url_for('login_router.login'))
    except Exception as e:
        print(f"Error fetching user: {e}")
        return redirect(url_for('login_router.login'))

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    if not check_password_hash(user['password'], current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('profile_router.profile'))

    hashed_password = generate_password_hash(new_password)
    users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'password': hashed_password}}
    )

    flash('Password updated successfully.', 'success')
    return redirect(url_for('profile_router.profile'))
