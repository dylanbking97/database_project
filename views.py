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

    # index should have bar at the top with nba visualizer or whatever to call it
    # should have explanation of what the app does
    # at the bottom: names of contributors
    # nba teams with logos as links to each team stat page.
    # also a search feature.
    # see current team stats.

#@app.route('/allstats')
#def

# takes user request and grabs team stats
@app.route('/team', methods=['GET'])
def team():

    if request.method == 'GET':

        # this grabs the user's search query from the HTML page into a python variable
        team = request.args['team']

        '''
        convert that to team name codes, i.e.
        "warriors" => 'GSW'
        '''
        team = convertName(team)
        if team == 'no matches':
            render_template(
                'index.html',
                teams=Teams.query.all()
            )

        else:
            selectedTeam = team
            FAsGained = FreeAgents.query.filter_by(newteam=selectedTeam)
            FAsLost = FreeAgents.query.filter_by(oldteam=selectedTeam)
            TDsGained = TradedPlayers.query.filter_by(newteam=selectedTeam)
            TDsLost = TradedPlayers.query.filter_by(oldteam=selectedTeam)
            DPs = DraftPicks.query.filter_by(team=selectedTeam)

            points = 0
            for FA in FAsGained:
                points += FA.points
            for TD in TDsGained:
                points += TD.points
            for DP in DPs:
                points += DP.points
            for FA in FAsLost:
                points -= FA.points
            for TD in TDsLost:
                points -= TD.points
            newPoints = round(points, 1)
            oldPoints = 0
            team = Teams.query.filter_by(name=selectedTeam)
            for oneteam in team:
                oldPoints += oneteam.points
            expectedPoints = round(oldPoints + newPoints, 1)

            rbs = 0
            for FA in FAsGained:
                rbs += FA.rebounds
            for TD in TDsGained:
                rbs += TD.rebounds
            for DP in DPs:
                rbs += DP.rebounds
            for FA in FAsLost:
                rbs -= FA.rebounds
            for TD in TDsLost:
                rbs -= TD.rebounds
            newRebounds = round(rbs, 2)
            oldRebounds = 0
            team = Teams.query.filter_by(name=selectedTeam)
            for oneteam in team:
                oldRebounds += oneteam.rebounds
            expectedRebounds = round(oldRebounds + newRebounds, 2)

            assts = 0
            for FA in FAsGained:
                assts += FA.assists
            for TD in TDsGained:
                assts += TD.assists
            for DP in DPs:
                assts += DP.assists
            for FA in FAsLost:
                assts -= FA.assists
            for TD in TDsLost:
                assts -= TD.assists
            newAssists = round(assts, 2)
            oldAssists = 0
            team = Teams.query.filter_by(name=selectedTeam)
            for oneteam in team:
                oldAssists += oneteam.assists
            expectedAssists = round(oldAssists + newAssists, 2)

            ws = 0
            for FA in FAsGained:
                ws += FA.winshares
            for TD in TDsGained:
                ws += TD.winshares
            for DP in DPs:
                ws += DP.winshares
            for FA in FAsLost:
                ws -= FA.winshares
            for TD in TDsLost:
                ws -= TD.winshares
            newWS = round(ws)
            oldWS = 0
            team = Teams.query.filter_by(name=selectedTeam)
            for oneteam in team:
                oldWS += oneteam.wins
            expectedWS = round(oldWS + newWS)

            expectedLS = 82 - expectedWS
            '''

            lost_players = [('Timofey Mozgov', 'BRK', 'ORL', '5.2', '4.2', '3.2', '0.4'), ('Dwight Howard', 'CHO', 'BRK', '16.6', '12.5', '1.3', '6.8')]
            gained_players = [('Timofey Mozgov', 'BRK', 'ORL', '5.2', '4.2', '3.2', '0.4'), ('Dwight Howard', 'CHO', 'BRK', '16.6', '12.5', '1.3', '6.8')]

            exp_pts = 5
            exp_rbs = 5
            exp_asts = 5
            expt_wins = 5
            '''

            #TODO: grouping of lost and gained players. for now just send in each group

            # this returns the appropriate template & queries the table
            return render_template(
                'team.html',
                team_row = Teams.query.filter_by(name=selectedTeam),
                team_logo_url=getLogoURL(selectedTeam),
                team_long_name=getLongName(selectedTeam),
                #lost_players=lost_players,
                #gained_players=gained_players,
                exp_pts=expectedPoints,
                pts=oldPoints,
                exp_rbs=expectedAssists,
                rbs=oldRebounds,
                exp_asts=expectedAssists,
                asts=oldAssists,
                exp_wins=expectedWS,
                wins=oldWS,
                exp_loss=expectedLS,
                FAsGained=FAsGained,
                FAsLost=FAsLost,
                TDsGained=TDsGained,
                TDsLost=TDsLost,
                DPs=DPs
            ) # queries the Team table
            # OR:
            # return render_template(
            #'advanced.html',
            #acquisitions = ASDF, lost_players = ASDF, exp_pt=ASDF, exp_reb=ASDF, exp_ast=ASDF, exp_rec=ASDF)
