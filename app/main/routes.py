from flask import render_template, url_for, redirect, request
from app import db
from models import Post, Event
from app.main import main
#from PIL import Image - non so perche non vada min 38.18 lezione 7


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int) #possiamo passare il numero di post che vogliamo per pagina
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #richiamo tutti i post
    events = Event.query.order_by(Event.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, events = events)



@main.route("/about")
def about():
    return render_template('about.html', title='About')



@main.route("/reset_db")
def reset_db():
    db.drop_all()
    db.create_all()
    return redirect(url_for('main.home'))