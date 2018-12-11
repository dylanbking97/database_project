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

# takes user request and grabs team stats
@app.route('/team', methods=['GET'])
def team():
    
    if request.method == 'GET':

        # this grabs the user's search query from the HTML page into a python variable
        team = request.args['team']

        '''
        TODO:convert that to team name codes, i.e.
        "warriors" => 'GSW'
        '''

        # this returns the appropriate template & queries the table
        return render_template(
        'basic.html',
        team_row = Teams.query.filter_by(name=team)) # queries the Team table
