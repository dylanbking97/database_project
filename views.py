from app import app
from models import Team
from flask import render_template, request

# Base page
@app.route('/')
def index():
    return render_template('index.html')
