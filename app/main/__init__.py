from flask import Blueprint

main = Blueprint('main', __name__) #passo il nome della mia blueprint

from app.main import routes