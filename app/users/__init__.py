from flask import Blueprint

users = Blueprint('users', __name__) #passo il nome della mia blueprint

from app.users import routes