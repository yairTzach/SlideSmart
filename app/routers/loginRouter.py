from flask import Blueprint, request, redirect, url_for, render_template, jsonify, current_app
import os

login_router = Blueprint('login_router', __name__)


@login_router.route('/login')
def login():
    return render_template('login.html')


