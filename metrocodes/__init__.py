from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')


# App Containers
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



@app.route('/', methods=['GET', ])
def handle_splash():
    return render_template('index.html')

from metrocodes.violations.views import mod as violationsModule
app.register_blueprint(violationsModule)
