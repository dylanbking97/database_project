from app import app
from models import db, Teams
from flask import render_template, request
from helpers import *

# dict mapping the long names to the abbreviations
teams = {"Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BRK",
        "Charlotte Hornets": "CHO",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHO",
        "Portland Trailblazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS"
        }

long_names = []

# loop through teams and place the long names in the list
for key in teams:
    long_names.append(key)

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
