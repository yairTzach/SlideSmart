from flask import Blueprint, request, redirect, url_for, render_template, jsonify, current_app
import os

register_router = Blueprint('register_router', __name__)

@register_router.route('/register')
def register():
    return render_template('register.html')
