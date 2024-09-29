from flask import Blueprint, redirect, url_for, make_response

# Define the Blueprint
logout_router = Blueprint('logout_router', __name__)

# Define the logout route
@logout_router.route('/logout')
def logout():
    response = make_response(redirect(url_for('login_router.login')))
    response.delete_cookie('userId', path='/')
    response.delete_cookie('username', path='/')
    return response
