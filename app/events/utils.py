from flask import url_for, current_app
from app import mail
import secrets
import os
from PIL import Image #non so perche non vada min 38.18 lezione 7
from flask_mail import Message

from models import JoinEvent


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path, 'static/events_pics', picture_fn)
    form_picture.save(picture_path)
    #return the name of the file we want to save in db
    return picture_fn
