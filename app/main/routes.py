from datetime import datetime


from flask import render_template, url_for, redirect, request

from app import db, bcrypt
from models import Post, Event, Business, User, JoinEvent, Private
from app.main import main
import app


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int) #possiamo passare il numero di post che vogliamo per pagina
    events = Event.query.order_by(Event.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', events = events)

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
        {'name': 'Giulia', 'surname': 'Borna'},
        {'name': 'Federico', 'surname': 'Marchini'},
        {'name': 'Chiara', 'surname': 'Martucci'}
    ]

    for user in users:
        email = user['name'].lower()+user['surname'].lower()+'@mail.com'
        username = user['name'].lower()+'_'+user['surname'].lower()
        telephone = 3397960955

        userdb = Private(name=user['name'], surname=user['surname'], email=email, password=bcrypt.generate_password_hash('1234567890').decode('utf-8'),
                         username=username, telephone=telephone)
        db.session.add(userdb)
        db.session.commit()

    businesses = [
        {'name': 'Azienda Colucci',  'city':'Alba', 'address':'via Vincenzo Gioberti, 63'},
        {'name': 'Rifugio La Marmotta', 'city':'Sestriere', 'address':'via Grazia Deledda, 38'},
        {'name': 'Cascina Belfiore', 'city': 'Sauze d Oulx', 'address': 'via Genova, 88'},
        {'name': 'Fratelli Rosselli', 'city': '', 'address':'via Salvemini, 12'},
        {'name': 'Ristorante Lenoci', 'city':'Casal Monferrato', 'address':'Corso Lecce, 58'}
    ]

    list_business = []
    for business in businesses:
        s = business['name'].replace(" ", "")
        email = s.lower() +'@mail.com'
        telephone = 3397960955
        vat_number = 123456
        c = Business(name=business['name'], email=email, password=bcrypt.generate_password_hash('1234567890').decode('utf-8'),
                     vat_number=vat_number,
                     city=business['city'], address=business['address'], telephone=telephone)
        list_business.append(c)
        db.session.add(c)
        events = [
            {'title': 'Degustazione formaggi', 'date': '2022-06-10', 'location':'Alba', 'price':15, 'equipment':'non richiesto', 'min_users':5, 'weaknesses':'no'},
            {'title': 'Ciaspolata + cena', 'date': '2022-05-03', 'location':'Alba', 'price':15, 'equipment':'non richiesto', 'min_users':5, 'weaknesses':'no'},
            {'title': 'Degustazione vini', 'date': '2022-04-25',  'location':'Alba', 'price':15, 'equipment':'non richiesto', 'min_users':5, 'weaknesses':'no'},
            {'title': 'Lago di Avigliana', 'date': '2022-04-25',  'location':'Alba', 'price':15, 'equipment':'non richiesto', 'min_users':5, 'weaknesses':'no'},
            {'title': 'Raccolta tartufi', 'date': '2022-04-25',  'location':'Alba', 'price':15, 'equipment':'non richiesto', 'min_users':5, 'weaknesses':'no'},
            {'title': 'Visita cantina', 'date': '2022-04-27',  'location':'Alba', 'price':15, 'equipment':'non richiesto', 'min_users':5, 'weaknesses':'no'}
        ]

    i = 0
    len_business = len(list_business)
    for event in events:
        if i<len_business:
            dt = datetime.strptime(event['date'], '%Y-%m-%d')
            e = Event(title=event['title'], date_event=dt, location=event['location'], price=event['price'],
                      equipment=event['equipment'], min_users=event['min_users'], content='null', weaknesses='null',
                      creator=list_business[i])
            i = i + 1
        db.session.add(e)
        db.session.commit()
    return redirect(url_for('users.logout'))

