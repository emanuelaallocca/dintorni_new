from datetime import datetime
from flask import render_template, url_for, redirect, request
from app import db, bcrypt
from models import Post, Event, Business, User, JoinEvent
from app.main import main
from PIL import Image #non so perche non vada min 38.18 lezione 7
from app import bcrypt


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

@main.route("/initialize_db")
def intialize_db():
    from flask_bcrypt import generate_password_hash
    db.drop_all()
    db.create_all()

    users = [
        {'name': 'Emanuela', 'surname':'Allocca'},
        {'name': 'Chiara', 'surname': 'Martucci'}
    ]

    for user in users:
        email = user['name'].lower()+user['surname'].lower()+'@mail.com'
        username = user['name'].lower()+'_'+user['surname'].lower()
        telephone = 3397960955

        userdb = User(name=user['name'], surname=user['surname'], email=email, password=bcrypt.generate_password_hash('1234567890').decode('utf-8'), username=username, telephone=telephone)
        db.session.add(userdb)
        db.session.commit()

    businesses = [
        {'name': 'amazon'},
        {'name': 'tesla'}
    ]

    for business in businesses:
        email = business['name'].lower()+'@mail.com'
        c = Business(name=business['name'], email=email, password=bcrypt.generate_password_hash('1234567890').decode('utf-8'))
        db.session.add(c)
        events = [
            {'title': 'nuovo evento', 'date': '2022-03-10'}
        ]

        for event in events:
            dt = datetime.strptime(event['date'], '%Y-%m-%d')
            e = Event(title=event['title'], date_event = dt, creator=c)
        db.session.add(e)
        db.session.commit()





    return redirect(url_for('users.logout'))