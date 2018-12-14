from app import app
from models import db, Teams, FreeAgents, DraftPicks, TradedPlayers
from flask import render_template, request
from helpers import *

# Base page
@app.route('/')
def index():
    selectedTeam = 'MIA'
    FAsGained=FreeAgents.query.filter_by(newteam=selectedTeam)
    FAsLost=FreeAgents.query.filter_by(oldteam=selectedTeam)
    TDsGained=TradedPlayers.query.filter_by(newteam=selectedTeam)
    TDsLost=TradedPlayers.query.filter_by(oldteam=selectedTeam)
    DPs= DraftPicks.query.filter_by(team=selectedTeam)

    points = 0
    for FA in FAsGained:
        points+= FA.points
    for TD in TDsGained:
        points+=TD.points
    for DP in DPs:
        points+=DP.points
    for FA in FAsLost:
        points-= FA.points
    for TD in TDsLost:
        points-=TD.points
    newPoints = round(points, 1)
    oldPoints=0
    team = Teams.query.filter_by(name=selectedTeam)
    for oneteam in team:
        oldPoints+=oneteam.points
    expectedPoints = round(oldPoints + newPoints, 1)

    rbs = 0
    for FA in FAsGained:
        rbs+= FA.rebounds
    for TD in TDsGained:
        rbs+=TD.rebounds
    for DP in DPs:
        rbs+=DP.rebounds
    for FA in FAsLost:
        rbs-= FA.rebounds
    for TD in TDsLost:
        rbs-=TD.rebounds
    newRebounds = round(rbs, 2)
    oldRebounds=0
    team = Teams.query.filter_by(name=selectedTeam)
    for oneteam in team:
        oldRebounds+=oneteam.rebounds
    expectedRebounds = round(oldRebounds + newRebounds, 2)

    assts = 0
    for FA in FAsGained:
        assts+= FA.assists
    for TD in TDsGained:
        assts+=TD.assists
    for DP in DPs:
        assts+=DP.assists
    for FA in FAsLost:
        assts-= FA.assists
    for TD in TDsLost:
        assts-=TD.assists
    newAssists = round(assts, 2)
    oldAssists=0
    team = Teams.query.filter_by(name=selectedTeam)
    for oneteam in team:
        oldAssists+=oneteam.assists
    expectedAssists = round(oldAssists + newAssists, 2)

    ws = 0
    for FA in FAsGained:
        ws+= FA.winshares
    for TD in TDsGained:
        ws+=TD.winshares
    for DP in DPs:
        ws+=DP.winshares
    for FA in FAsLost:
        ws-= FA.winshares
    for TD in TDsLost:
        ws-=TD.winshares
    newWS = round(ws)
    oldWS=0
    team = Teams.query.filter_by(name=selectedTeam)
    for oneteam in team:
        oldWS+=oneteam.wins
    expectedWS = round(oldWS + newWS)

    expectedLS = 82-expectedWS


    return render_template(
    'index.html', teams=Teams.query.all(),
    oldPoints=oldPoints, expectedPoints=expectedPoints,
    oldRebounds=oldRebounds, expectedRebounds=expectedRebounds,
    oldAssists=oldAssists, expectedAssists=expectedAssists,
    oldWS=oldWS, expectedWS=expectedWS, expectedLS=expectedLS,
    FAsGained=FAsGained, FAsLost=FAsLost, DPs=DPs,
    TDsGained=TDsGained, TDsLost=TDsLost)

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
        team_row = Teams.query.filter_by(name=team), # queries the Team table
        newPlayers = allPlayers.query.filter_by(newteam=team), # queries the players table
        oldplayers = allPlayers.query.filter_by(oldteam=team))
