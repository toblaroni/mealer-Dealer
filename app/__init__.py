from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.loop_variables = 'all'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)

from app import views, models