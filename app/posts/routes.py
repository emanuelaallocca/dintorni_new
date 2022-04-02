from datetime import datetime

from flask import render_template, url_for, flash, redirect, request, abort
from app import db
from app.posts.forms import PostForm
from models import Post, JoinEvent, Event
from flask_login import current_user, login_required
from app.posts import posts
from app.events import events


#from PIL import Image - non so perche non vada min 38.18 lezione 7


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    jevents = JoinEvent.query.filter_by(user_id=current_user.id).all()
    events_already_done = []
    for e in jevents:
        ev = Event.query.filter_by(id=e.event_id).first()
        if ev:
            if ev.date_event < datetime.today().date():
                events_already_done.append(ev)
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, event_title = form.event_title.data)
        db.session.add(post)
        db.session.commit()
        flash('post created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', events = events_already_done, ea_tot = len(events_already_done))

@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='Post', post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403) #risposta per forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit() #sto solo aggiornando qualcosa che c'è già
        flash('update done', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
    form.title.data=post.title
    form.content.data=post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/reviews", methods=['GET', 'POST'])
def reviews():
    page = request.args.get('page', 1, type=int)  # possiamo passare il numero di post che vogliamo per pagina
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #richiamo tutti i post
    return render_template('comments.html', posts=posts)


