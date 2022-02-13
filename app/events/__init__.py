from flask import Blueprint

events = Blueprint('events', __name__) #passo il nome della mia blueprint

from app.events import routes