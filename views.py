from app import app
from models import db, Teams
from flask import render_template, request
from helpers import *

# Base page
@app.route('/')
def index():
    return render_template(
    'index.html',
    teams=Teams.query.all())
