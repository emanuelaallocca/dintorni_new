from flask import Blueprint

posts = Blueprint('posts', __name__) #passo il nome della mia blueprint

from app.posts import routes