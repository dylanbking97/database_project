from flask_sqlalchemy import SQLAlchemy
from app import app

# configures the app to use a postgresql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nba'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Team stats for 2017-2018
class Teams(db.Model):
    __tablename__ = "teams"
    name = db.Column(db.String(120), primary_key=True)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)

    # declare relationships to other Tables
    last_season = db.relationship('Teams16_17', backref='last_season_teams', lazy=True)
    draftpicks = db.relationship('DraftPicks', backref='dp_teams', lazy=True)
    freeagents = db.relationship('FreeAgents', backref='fa_teams', lazy=True)
    tradedplayers = db.relationship('FreeAgents', backref='tp_teams', lazy=True)

class Teams16_17(db.Model):
    __tablename__ = "teams16_17"
    name = db.Column(db.String(120), db.ForeignKey('teams.name'), primary_key=True)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)

class DraftPicks(db.Model):
    __tablename__ = "draftpicks"
    name = db.Column(db.String(120), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    winshares = db.Column(db.Float, nullable=False)

    # declare team name as foreign key
    team = db.Column(db.String(120), db.ForeignKey('teams.name'),
    nullable=False)

# table for free agents.
class FreeAgents(db.Model):
    __tablename__ = "freeagents"
    name = db.Column(db.String(120), primary_key=True)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    winshares = db.Column(db.Float, nullable=False)
    oldteam = db.Column(db.String(120), nullable=False)

    # declare team name as foreign key
    newteam = db.Column(db.String(120), db.ForeignKey('teams.name'),
    nullable=False)


class TradedPlayers(db.Model):
    __tablename__ = "tradedplayers"
    name = db.Column(db.String(120), primary_key=True)
    points = db.Column(db.Float, nullable=False)
    rebounds = db.Column(db.Float, nullable=False)
    assists = db.Column(db.Float, nullable=False)
    winshares = db.Column(db.Float, nullable=False)
    oldteam = db.Column(db.String(120), nullable=False)

    # declare team name as foreign key
    newteam = db.Column(db.String(120), db.ForeignKey('teams.name'),
    nullable=False)
