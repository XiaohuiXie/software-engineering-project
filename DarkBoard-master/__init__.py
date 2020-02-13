# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pymongo import PyMongo
from DarkBoard.backend import Backend


app = Flask(__name__)
app.config["MONGO_URI"] = "127.0.0.01/DarkBoard"
app.secret_key = '4ijfw4KK4w9jvkrn$'
db = PyMongo(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
Backend = Backend(db)


from DarkBoard.user import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User(int(user_id))

# blueprint for auth routes in our app
from DarkBoard.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from DarkBoard.main import main as main_blueprint
app.register_blueprint(main_blueprint)

