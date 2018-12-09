from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.heroku import Heroku


# boilerplate code
app = Flask(__name__)
heroku = Heroku(app)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
