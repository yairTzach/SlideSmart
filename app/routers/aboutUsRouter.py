from flask import Blueprint, request, redirect, url_for, render_template, jsonify, current_app
import os

aboutUs_router = Blueprint('aboutUs_router', __name__)

@aboutUs_router.route('/')
def openningPage():
    return render_template('aboutUs.html')

@aboutUs_router.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

