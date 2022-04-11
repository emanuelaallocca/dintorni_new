from datetime import datetime


from flask import render_template, url_for, redirect, request

from app import db, bcrypt
from models import Post, Event, Business, User, JoinEvent, Private
from app.main import main
import app


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date_event.desc()).paginate(page=page, per_page=10)
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
        {'name': 'Chiara', 'surname': 'Martucci'},
        {'name': 'Giorgio', 'surname': 'Aruta'}
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
        {'name': 'Mara Wine Resort', 'city': 'Bra', 'address': 'via Genova, 88'},
        {'name': 'Fratelli Rosselli', 'city': 'Avigliana', 'address':'via Salvemini, 12'},
        {'name': 'Ristorante Lenoci', 'city':'Barolo', 'address':'Corso Lecce, 58'},
        {'name': 'Turin Wake Park', 'city': 'Settimo Torinese', 'address': 'Via Nicolo Paganini, 49'}
    ]

    list_business = []
    for business in businesses:
        s = business['name'].lower().replace(" ", "")
        email = s.lower() +'@mail.com'
        telephone = 3397960955
        vat_number = 12345678911
        c = Business(name=business['name'], email=email, password=bcrypt.generate_password_hash('1234567890').decode('utf-8'),
                     vat_number=vat_number,
                     city=business['city'], address=business['address'], telephone=telephone)
        list_business.append(c)
        db.session.add(c)
        events = [
            {'title': 'Cheeses tasting', 'date': '2022-06-10', 'location':'Alba', 'price':15,
             'equipment':'Not required', 'min_users':5, 'weaknesses':'Lactose',
             'content':'Bring a big appetite, as you can sample 10 cheeses and 10 wines, as well as a full Piedmont-style lunch. '
                       'You will see the vineyards and olive trees that are used to produce our olive oil. '
                       'Our first stop will be an authentic farm where pecorino and other cheeses are produced. '
                       'We will show you the machinery used to make the cheese and then you can taste the cheese and pair it with the own wine.',
             'image_event1':'event1_12.jpg', 'image_event2':'event1_2.jpg', 'image_event3':'evento1_33.png'},

            {'title': 'Snowshoeing + lunch', 'date': '2022-05-03', 'location':'Sestriere', 'price':'40', 'equipment':'Mountain clothing', 'min_users':5, 'weaknesses':'Vertigo',
             'content': 'Half-day snowshoe hike on the snows of the Susa Valley. '
                        'Level: +100 mt - 100 mt. Development: 4 km. Points of interest: alpine environment, possible sighting of wild animals. ' 
                        'Immersed in the wilderness of the park we will enjoy the soft snow, the panorama of a 2200m of the Susa Valley and at the end, if you wish, a good polenta.' 
                        ' Morning hike at 10am.' 
                        ' Afternoon hike at 2 pm.', 'image_event1': 'event1_12.jpg', 'image_event2': 'event1_2.jpg', 'image_event3': 'evento1_33.png',
             'image_event1':'event2_12345.jpg', 'image_event2':'event2_2.jpg', 'image_event3':'event2_3.jpg'},

            {'title': 'Wines tasting', 'date': '2022-04-25',  'location':'Bra', 'price':15, 'equipment':'Camera suggested', 'min_users':2, 'weaknesses':'no',
             'content': 'We will start the tour on the terrace of Merumalia Wine Resort, my winery. I will introduce you to the history of the winery with a breathtaking view of the vineyards and Rome. We will walk through the vineyards, immersed in its colours. We will then visit the winery and I will explain our production philosophy. The tour continues with a tasting of our organic wines, which have been awarded by the major wine guides. The tasting will be combined with local and organic cheeses and cold cuts.',
             'image_event1':'event3_1.jpg', 'image_event2':'event3_2.jpg', 'image_event3':'event3_3.jpg'},

            {'title': 'Avigliana Lakes', 'date': '2022-04-25',  'location':'Avigliana', 'price':45, 'equipment':'Not required', 'min_users':5, 'weaknesses':'Seasickness',
             'content': 'Boat shared with other people, lasting an hour and a half (1.5h), during which there will be a description in various languages (Italian, English) of the beautiful villas and the main attractions that can only be enjoyed from the lake from a boat, with the possibility to linger and enjoy the wonderful scenery and take unique photographs from the perspective of the lake in absolute tranquillity.',
             'image_event1':'event4_1.jpg', 'image_event2':'event4_2.jpg', 'image_event3':'event4_3.png'},

            {'title': 'Harvesting Truffles', 'date': '2022-04-25',  'location':'Barolo', 'price':15, 'equipment':'Not required', 'min_users':5, 'weaknesses':'No',
             'content': 'In order to tell the story of our work, the truffle and its legends, we have decided to give our customers the opportunity to experience the search for both white and black truffles. Our truffle hunts take place in natural truffle grounds according to the growing season and the regional truffle hunting calendar, and are rich in educational and historical content so that you can return home with a true cultural and experiential heritage of the truffle.',
             'image_event1': 'event5_1.jpg', 'image_event2': 'event5_2.jpg', 'image_event3': 'event5_3.png'},

            {'title': 'Wakeboard on artificial lake', 'date': '2022-03-27',  'location':'Settimo Torinese', 'price':30, 'equipment':'Swimwear', 'min_users':1, 'weaknesses':'No',
             'content': 'Have you ever wanted to try wakeboarding or wake surfing? Come and have a look and see how much fun it is to be in the water. You can even go tubing if you want. All travellers are welcome, from beginners to experts. During your experience you can stand on the board and take a wakeboard ride on your own, but most importantly, you will enjoy incredible energy surrounded by nature.',
             'image_event1':'event6_5.png', 'image_event2':'event6_2.jpg', 'image_event3':'event6_3.jpg'}
        ]

    i = 0
    len_business = len(list_business)
    for event in events:
        if i<len_business:
            dt = datetime.strptime(event['date'], '%Y-%m-%d')
            e = Event(title=event['title'], date_event=dt, location=event['location'], price=event['price'],
                      equipment=event['equipment'], min_users=event['min_users'], content=event['content'], weaknesses=event['weaknesses'],
                      image_event1 = event['image_event1'], image_event2 = event['image_event2'], image_event3 = event['image_event3'],
                      creator=list_business[i])
            i = i + 1
        db.session.add(e)
        db.session.commit()

    join_event = JoinEvent(event_id = 6, user_id = 1,transport_type = 'bus', time_hour = 0, time_minute = 0,place='null', number_of_seats = 0 )
    db.session.add(join_event)
    db.session.commit()

    return redirect(url_for('users.logout'))

