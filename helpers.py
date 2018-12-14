from urllib.request import urlopen
from bs4 import BeautifulSoup
from models import db, Teams, Teams16_17, DraftPicks, FreeAgents, TradedPlayers

#gets html of webpage
#BeautifulSoup turns html into an easily traversible html object

def addDraftPicks():
    #Get data from all draft picks
    html = urlopen("https://www.basketball-reference.com/draft/NBA_2018.html")
    bsObj = BeautifulSoup(html, "lxml")

    rows = bsObj.tbody.findAll("tr")
    alltabledata = []
    for player in rows:
        alltabledata.append(player.find_all("td"))#.get_text())

    #draftpicks is a list full of tuples containing each draft pick's statistics (pts, rbs, assts, win shares, etc.)
    draftpicks = []
    for player in range(30):
        #only count draft picks who have played more than 5 games this season
        if((alltabledata[player][5].get_text() != "") and (int(alltabledata[player][5].get_text()) >5)):
            #estimated win share value for a full season (~75 games)
            expectedwinshares = round((75/int(alltabledata[player][5].get_text())) * (float(alltabledata[player][17].get_text())), 1)
            playerinfo = (alltabledata[player][2].get_text(), 2018, alltabledata[player][1].get_text(),
                          alltabledata[player][14].get_text() , alltabledata[player][15].get_text(),
                          alltabledata[player][16].get_text(), expectedwinshares)
            draftpicks.append(playerinfo)

    for player in range(32, 62):
        if((alltabledata[player][5].get_text() != "") and (int(alltabledata[player][5].get_text()) >5)):
            expectedwinshares = round((75/int(alltabledata[player][5].get_text())) * (float(alltabledata[player][17].get_text())), 1)
            playerinfo = (alltabledata[player][2].get_text(), 2018, alltabledata[player][1].get_text(),
                          alltabledata[player][14].get_text() , alltabledata[player][15].get_text(),
                          alltabledata[player][16].get_text(), expectedwinshares)
            draftpicks.append(playerinfo)


    # code to add draft picks to the database
    # loop through draftpicks list and add + commit each player to the databse
    for player in draftpicks:
        pick = DraftPicks(name=player[0], year=player[1], team=player[2], points=player[3],
         rebounds=player[4], assists=player[5], winshares=player[6])
        db.session.add(pick)
        db.session.commit()

    #print(draftpicks)
    #print(len(draftpicks))

def addFreeAgents():
    #get data from all free agents who switched teams
    html = urlopen("https://www.basketball-reference.com/friv/free_agents.cgi?year=2018")
    FAbsObj = BeautifulSoup(html, "lxml")

    FArows = FAbsObj.tbody.findAll("tr")
    FAtabledata = []

    for player in FArows:
        FAtabledata.append(player.find_all("td"))

    #freeagents is a list of tuples containing each free agents old team/new team, stats
    freeagents = []
    x,y = 0,20
    for loop in range(8):
        for player in range(x,y):
            if ((FAtabledata[player][4].get_text() != FAtabledata[player][7].get_text())):# and (FAtabledata[player][7].get_text() != '')):
                name = FAtabledata[player][0].get_text()
                oldteam = FAtabledata[player][4].get_text()
                newteam = FAtabledata[player][7].get_text()
                playerinfo = (FAtabledata[player][5].get_text())
                splitstats = playerinfo.split(", ")
                pts = splitstats[0][0:4].strip()
                rbs = splitstats[1][0:4].strip()
                asts = splitstats[2][0:4].strip()
                winshares = FAtabledata[player][6].get_text()
                FAstats = (name, oldteam, newteam, pts, rbs, asts, winshares)
                freeagents.append(FAstats)
        x +=21
        y +=21

    # loops through freeagents list and adds each player to the database
    for fa in freeagents:

        # only add to database if the free agent has been signed
        if fa[2]:
            agent = FreeAgents(name=fa[0], oldteam=fa[1], newteam=fa[2], points=fa[3],
             rebounds=fa[4], assists=fa[5], winshares=fa[6])

            # add and commit the player to the database
            db.session.add(agent)
            db.session.commit()

    #print(freeagents)
    #print(len(freeagents))

trades = [('Timofey Mozgov', 'BRK', 'ORL', '5.2', '4.2', '3.2', '0.4'), ('Dwight Howard', 'CHA', 'BRK', '16.6', '12.5', '1.3', '6.8'),
 ('Hamidou Diallo', 'BRK', 'OKC', '5.9', '2.7', '0.5', '3.1'),('Shai Gilgeous-Alexander', 'CHO', 'LAC', '13.4', '3.3', '3.0', '3.8'),
 ('Miles Bridges', 'LAC', 'CHO', '8.0', '4.0', '1.0', '4.0'), ("Devonte' Graham", 'ATL', 'CHO', '2.4', '0.7', '1.3', '0.0'),
 ('Mikal Bridges', 'PHI', 'PHO', '6.8', '2.2', '1.1', '1.2'), ('Luke Doncic', 'ATL', 'DAL', '18.1', '6.5', '4.3', '3.8'),
 ('Trae Young', 'DAL', 'ATL', '15.7', '2.8', '7.3', '-2.5'), ('Austin Rivers', 'LAC', 'WAS', '15.1', '2.4', '4.0', '-0.3'),
 ('Marcin Gortat', 'WAS', 'LAC', '8.4', '7.6', '1.8', '4.9'), ('Wilson Chandler', 'DEN', 'PHI', '10.0', '5.4', '2.1', '3.3'),
 ('Bismack Biyombo', 'ORL', 'CHO', '5.7', '5.7', '0.8', '2.9'),('Jerian Grant', 'CHI', 'ORL', '8.4', '2.3', '4.6', '3.3'),
 ('Jeremy Lin', 'BRK', 'ATL', '14.5', '3.8', '5.1', '2.1'), ('Kennth Faried', 'DEN', 'BRK', '5.9', '4.8', '0.6', '1.3'),
 ('Garrett Temple', 'SAC', 'MEM', '8.4', '2.3', '1.9', '1.2'), ('Ben McLemore', 'MEM', 'SAC', '7.5', '2.5', '0.9','0.5'),
 ('Kawhi Leonard', 'SAS', 'TOR', '25.5', '3.8', '5.5', '13.6'), ('DeMar DeRozan', 'TOR', 'SAS', '23.0', '3.9', '3.2','9.6'),
 ('Danny Green', 'SAS', 'TOR', '8.6', '3.6', '1.6', '2.9'), ('Justin Anderson', 'PHI', 'ATL', '6.2', '2.4', '0.7', '1.2'),
 ('Dennis Schroder', 'ATL', 'OKC', '19.1', '3.4', '6.2', '2.6'), ('Mike Muscala', 'ATL', 'PHI', '7.6', '4.3', '1.0', '2.4'),
 ('Richaun Holmes', 'PHI', 'PHO', '6.5', '4.4', '1.3', '2.8'), ('Jared Dudley', 'PHO', 'BRK', '3.2', '2.0', '1.6', '0.8'),
 ('Jarell Martin', 'MEM', 'ORL', '7.7', '4.4', '1.0', '1.3'), ('Sam Dekker', 'LAC', 'CLE', '4.2', '2.4', '0.5', '1.2'),
 ('Ryan Anderson', 'HOU', 'PHO', '9.3', '5.0', '0.9', '4.8'), ('Wesley Johnson', 'LAC', 'NOP', '5.4', '2.9', '0.8', '1.7'),
 ('Jimmy Butler', 'MIN', 'PHI', '22.2', '5.3', '4.9', '8.9'), ('Dario Saric', 'PHI', 'MIN', '14.6', '6.7', '2.6', '6.6'),
 ('Robert Covington', 'PHI', 'MIN', '12.6', '5.4', '2.0', '6.1'), ('Alec Burks', 'UTA', 'CLE', '7.7', '3.0', '1.0', '1.9'),
 ('Kyle Korver', 'CLE', 'UTA', '9.3', '2.3', '1.2', '3.4')]
#print(len(trades))

# function to add traded players to the database
def addTradedPlayers():

    # loop through the trades list and add the values to the database
    for player in trades:

        trade = TradedPlayers(name=player[0], oldteam=player[1], newteam=player[2], points=player[3],
         rebounds=player[4], assists=player[5], winshares=player[6])
        db.session.add(trade)
        db.session.commit()

sixers = []
lost = []
teams = ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM',
        'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
#team = "GSW"
#for player in trades:
#    if(player[2] == team):
#        sixers.append(player)
#for player in freeagents:
#    if(player[2] == team):
#        sixers.append(player)
#for player in draftpicks:
#    if(player[2] == team):
#        sixers.append(player)
#for player in trades:
#    if(player[1] == team):
#        lost.append(player)
#for player in freeagents:
#    if(player[1] == team):
#        lost.append(player)
#for player in draftpicks:
#    if(player[1] == team):
#        lost.append(player)
#for player in sixers:
#    print(player[0], player[6])
#print("lost:")
#for player in lost:
#    print(player[0], player[6])


def addTeams():
    #Tables with each teams win-loss record, basic stats for each of the last two seasons
    teams = ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM',
            'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

    teams201718 = []
    teams201617 = []
    for team in range(30):
        html = urlopen("https://www.basketball-reference.com/teams/%s/stats_per_game_totals.html" % teams[team])
        teamObj = BeautifulSoup(html, "lxml")


        team201819 = teamObj.tbody.find("tr")
        team201718 = team201819.find_next("tr")
        team201617 = team201718.find_next("tr")
        teamstats = team201718.findAll("td")
        teamstats1 = team201617.findAll("td")
        name, name1 = teamstats[1].get_text(), teamstats1[1].get_text()
        wins, wins1 = teamstats[2].get_text(), teamstats1[2].get_text()
        losses, losses1 = teamstats[3].get_text(), teamstats1[3].get_text()
        points, points1 = teamstats[32].get_text(), teamstats1[32].get_text()
        rbs, rbs1 = teamstats[26].get_text(), teamstats1[26].get_text()
        assts, assts1 = teamstats[27].get_text(), teamstats1[27].get_text()
        stattuple, stattuple1 = (name, wins, losses, points, rbs, assts), (name1, wins1, losses1, points1, rbs1, assts1)

        teams201718.append(stattuple)
        #teams201617.append(stattuple1)

    # inserts team data in the database for 17-18 season
    for team in teams201718:

        team_stats = Teams(name=team[0], wins=team[1], losses=team[2], points=team[3], rebounds=team[4], assists=team[5])
        db.session.add(team_stats)

    # commits the changes made to the database
    db.session.commit()

    #print(teams201617)

def getLogoURL(name):
    name = name.upper()
    url_catalog = {'ATL': "http://content.sportslogos.net/logos/6/220/thumbs/22091682016.gif",
                   'BOS': "http://content.sportslogos.net/logos/6/213/thumbs/slhg02hbef3j1ov4lsnwyol5o.gif",
                   'BRK': "http://content.sportslogos.net/logos/6/3786/thumbs/hsuff5m3dgiv20kovde422r1f.gif",
                   'CHO': "http://content.sportslogos.net/logos/6/5120/thumbs/512019262015.gif",
                   'CHI': "http://content.sportslogos.net/logos/6/221/thumbs/hj3gmh82w9hffmeh3fjm5h874.gif",
                   'CLE': "http://content.sportslogos.net/logos/6/222/thumbs/22269212018.gif",
                   'DAL': "http://content.sportslogos.net/logos/6/228/thumbs/22834632018.gif",
                   'DEN': "http://content.sportslogos.net/logos/6/229/thumbs/22989262019.gif",
                   'DET': "http://content.sportslogos.net/logos/6/223/thumbs/22321642018.gif",
                   'GSW': "http://content.sportslogos.net/logos/6/235/thumbs/qhhir6fj8zp30f33s7sfb4yw0.gif",
                   'HOU': "http://content.sportslogos.net/logos/6/230/thumbs/8xe4813lzybfhfl14axgzzqeq.gif",
                   'IND': "http://content.sportslogos.net/logos/6/224/thumbs/22448122018.gif",
                   'LAC': "http://content.sportslogos.net/logos/6/236/thumbs/23654622016.gif",
                   'LAL': "http://content.sportslogos.net/logos/6/237/thumbs/uig7aiht8jnpl1szbi57zzlsh.gif",
                   'MEM': "http://content.sportslogos.net/logos/6/231/thumbs/23143732019.gif",
                   'MIA': "http://content.sportslogos.net/logos/6/214/thumbs/burm5gh2wvjti3xhei5h16k8e.gif",
                   'MIL': "http://content.sportslogos.net/logos/6/225/thumbs/22582752016.gif",
                   'MIN': "http://content.sportslogos.net/logos/6/232/thumbs/23296692018.gif",
                   'NOP': "http://content.sportslogos.net/logos/6/4962/thumbs/496226812014.gif",
                   'NYK': "http://content.sportslogos.net/logos/6/216/thumbs/2nn48xofg0hms8k326cqdmuis.gif",
                   'OKC': "http://content.sportslogos.net/logos/6/2687/thumbs/khmovcnezy06c3nm05ccn0oj2.gif",
                   'ORL': "http://content.sportslogos.net/logos/6/217/thumbs/wd9ic7qafgfb0yxs7tem7n5g4.gif",
                   'PHI': "http://content.sportslogos.net/logos/6/218/thumbs/21870342016.gif",
                   'PHO': "http://content.sportslogos.net/logos/6/238/thumbs/23843702014.gif",
                   'POR': "http://content.sportslogos.net/logos/6/239/thumbs/23997252018.gif",
                   'SAC': "http://content.sportslogos.net/logos/6/240/thumbs/24040432017.gif",
                   'SAS': "http://content.sportslogos.net/logos/6/233/thumbs/23325472018.gif",
                   'TOR': "http://content.sportslogos.net/logos/6/227/thumbs/22745782016.gif",
                   'UTA': "http://content.sportslogos.net/logos/6/234/thumbs/23467492017.gif",
                   'WAS': "http://content.sportslogos.net/logos/6/219/thumbs/21956712016.gif"
                   }
    if name in url_catalog:
        return url_catalog[name]
    else:
        return 'no matches'

def convertName(name):
    name_catalog = {'ATL': ['ATLANTA HAWKS', 'ATLANTA', 'HAWKS', 'ATL'],
                    'BOS': ['BOSTON CELTICS', 'BOSTON', 'CELTICS', 'BOS'],
                    'BRK': ['NEW JERSEY NETS', 'NEW JERSEY', 'NETS', 'BROOKLYN NETS', 'BROOKLYN', 'BKN', 'BRK', 'NJN'],
                    'CHO': ['CHARLOTTE HORNETS', 'CHARLOTTE', 'HORNETS', 'CHH', 'CHO', 'CHA'],
                    'CHI': ['CHICAGO BULLS', 'CHICAGO', 'BULLS', 'CHI'],
                    'CLE': ['CLEVELAND CAVALIERS', 'CLEVELAND', 'CAVALIERS','CLE'],
                    'DAL': ['DALLAS MAVERICKS', 'DALLAS', 'MAVERICKS', 'DAL'],
                    'DEN': ['DENVER NUGGETS', 'DENVER', 'NUGGETS', 'DEN'],
                    'DET': ['DETROIT PISTONS', 'DETROIT', 'PISTONS', 'DET'],
                    'GSW': ['GOLDEN STATE WARRIORS', 'GOLDEN STATE', 'WARRIORS', 'GSW'],
                    'HOU': ['HOUSTON ROCKETS', 'HOUSTON', 'ROCKETS', 'HOU'],
                    'IND': ['INDIANA PACERS', 'INDIANA', 'PACERS', 'IND'],
                    'LAC': ['LOS ANGELES CLIPPERS', 'CLIPPERS', 'LAC'],
                    'LAL': ['LOS ANGELES LAKERS', 'LOS ANGELES', 'LAKERS', 'LAL'],
                    'MEM': ['MEMPHIS GRIZZLIES', 'MEMPHIS', 'GRIZZLIES', 'MEM'],
                    'MIA': ['MIAMI HEAT', 'MIAMI', 'HEAT', 'MIA'],
                    'MIL': ['MILWAUKEE BUCKS', 'MILWAUKEE', 'BUCKS', 'MIL'],
                    'MIN': ['MINNESOTA TIMBERWOLVES', 'MINNESOTA', 'TIMBERWOLVES', 'MIN'],
                    'NOP': ['NEW ORLEANS PELICANS', 'NEW ORLEANS', 'PELICANS', 'NOP'],
                    'NYK': ['NEW YORK KNICKS', 'NEW YORK', 'KNICKS', 'NYK'],
                    'OKC': ['OKLAHOMA CITY THUNDER', 'OKLAHOMA CITY', 'THUNDER', 'OKC'],
                    'ORL': ['ORLANDO MAGIC', 'ORLANDO', 'MAGIC', 'ORL'],
                    'PHI': ['PHILADELPHIA 76ERS', 'PHILADELPHIA', '76ERS', 'PHI'],
                    'PHO': ['PHOENIX SUNS', 'PHOENIX', 'SUNS', 'PHO', 'PHX'],
                    'POR': ['PORTLAND TRAIL BLAZERS', 'PORTLAND', 'TRAIL BLAZERS', 'POR'],
                    'SAC': ['SACRAMENTO KINGS', 'SACRAMENTO', 'KINGS', 'SAC'],
                    'SAS': ['SAN ANTONIO SPURS', 'SAN ANTONIO', 'SPURS', 'SAS'],
                    'TOR': ['TORONTO RAPTORS', 'TORONTO', 'RAPTORS', 'TOR'],
                    'UTA': ['UTAH JAZZ', 'UTAH', 'JAZZ', 'UTA'],
                    'WAS': ['WASHINGTON WIZARDS', 'WASHINGTON', 'WIZARDS', 'WAS']
                    }
    name = name.upper()
    for code, matches in name_catalog.items():
        if name in matches:
            return code
    return 'no matches'

def getLongName(name):
    name_catalog = {'ATL': ['ATLANTA HAWKS', 'ATLANTA', 'HAWKS', 'ATL'],
                    'BOS': ['BOSTON CELTICS', 'BOSTON', 'CELTICS', 'BOS'],
                    'BRK': ['NEW JERSEY NETS', 'NEW JERSEY', 'NETS', 'BROOKLYN NETS', 'BROOKLYN', 'BKN', 'BRK', 'NJN'],
                    'CHO': ['CHARLOTTE HORNETS', 'CHARLOTTE', 'HORNETS', 'CHH', 'CHO', 'CHA'],
                    'CHI': ['CHICAGO BULLS', 'CHICAGO', 'BULLS', 'CHI'],
                    'CLE': ['CLEVELAND CAVALIERS', 'CLEVELAND', 'CAVALIERS', 'CLE'],
                    'DAL': ['DALLAS MAVERICKS', 'DALLAS', 'MAVERICKS', 'DAL'],
                    'DEN': ['DENVER NUGGETS', 'DENVER', 'NUGGETS', 'DEN'],
                    'DET': ['DETROIT PISTONS', 'DETROIT', 'PISTONS', 'DET'],
                    'GSW': ['GOLDEN STATE WARRIORS', 'GOLDEN STATE', 'WARRIORS', 'GSW'],
                    'HOU': ['HOUSTON ROCKETS', 'HOUSTON', 'ROCKETS', 'HOU'],
                    'IND': ['INDIANA PACERS', 'INDIANA', 'PACERS', 'IND'],
                    'LAC': ['LOS ANGELES CLIPPERS', 'CLIPPERS', 'LAC'],
                    'LAL': ['LOS ANGELES LAKERS', 'LOS ANGELES', 'LAKERS', 'LAL'],
                    'MEM': ['MEMPHIS GRIZZLIES', 'MEMPHIS', 'GRIZZLIES', 'MEM'],
                    'MIA': ['MIAMI HEAT', 'MIAMI', 'HEAT', 'MIA'],
                    'MIL': ['MILWAUKEE BUCKS', 'MILWAUKEE', 'BUCKS', 'MIL'],
                    'MIN': ['MINNESOTA TIMBERWOLVES', 'MINNESOTA', 'TIMBERWOLVES', 'MIN'],
                    'NOP': ['NEW ORLEANS PELICANS', 'NEW ORLEANS', 'PELICANS', 'NOP'],
                    'NYK': ['NEW YORK KNICKS', 'NEW YORK', 'KNICKS', 'NYK'],
                    'OKC': ['OKLAHOMA CITY THUNDER', 'OKLAHOMA CITY', 'THUNDER', 'OKC'],
                    'ORL': ['ORLANDO MAGIC', 'ORLANDO', 'MAGIC', 'ORL'],
                    'PHI': ['PHILADELPHIA 76ERS', 'PHILADELPHIA', '76ERS', 'PHI'],
                    'PHO': ['PHOENIX SUNS', 'PHOENIX', 'SUNS', 'PHO', 'PHX'],
                    'POR': ['PORTLAND TRAIL BLAZERS', 'PORTLAND', 'TRAIL BLAZERS', 'POR'],
                    'SAC': ['SACRAMENTO KINGS', 'SACRAMENTO', 'KINGS', 'SAC'],
                    'SAS': ['SAN ANTONIO SPURS', 'SAN ANTONIO', 'SPURS', 'SAS'],
                    'TOR': ['TORONTO RAPTORS', 'TORONTO', 'RAPTORS', 'TOR'],
                    'UTA': ['UTAH JAZZ', 'UTAH', 'JAZZ', 'UTA'],
                    'WAS': ['WASHINGTON WIZARDS', 'WASHINGTON', 'WIZARDS', 'WAS']
                    }
    name = name.upper()
    if name in name_catalog:
        return name_catalog[name][0]
    else:
        return 'no matches'
