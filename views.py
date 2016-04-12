# -*- coding: utf-8 -*-

import datetime

from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    request,
    render_template,
    jsonify
)
from flask.ext.login import login_required, current_user
from flask_mail import Message
from forms import PostForm, BackwardForm, CommentForm
from models import User, Post, Comment
from app import db, mail

blog = Blueprint('blog', __name__)
# admin = Blueprint('admin', __name__, url_prefix='/admin')
# https://github.com/apiguy/flask-classy


# Views:


@blog.route('/', methods=['GET', 'POST'])
def home():
    visible_posts = Post.query.filter_by(is_visible=True).all()
    return render_template(
        'home.html', posts=visible_posts)


@blog.route('/view_post', methods=['POST'])
def view_post():
    if request.method == 'POST':
        post_id = request.form['id']
        post = Post.query.filter_by(id=post_id).first()
        comments = Comment.query.filter_by(post_id=post_id).all() # TODO: query comments from DB
        form = CommentForm()
        return render_template('post.html', form=form, post=post, comments=comments)


@blog.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        form = PostForm(request.form)
        if form.validate():
            print(type(user))
            form.user = user
            post = Post(user=user, **form.data)
            db.session.add(post)
            db.session.commit()
            post_title = Post.query.filter_by(title=post.title).first().title
            flash('Post "{}" created!'.format(post_title))
            return redirect(url_for('blog.home'))

    form = PostForm()

    return render_template(
        'new_post.html', form=form)


@blog.route('/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post():
    # if request.method == 'POST':
    #     user = User.query.filter_by(username=current_user.username).first()
    #     form = PostForm(request.form)
    #     if form.validate():
    #         form.user = user
    #         post = Post(user=user, **form.data)
    #         db.session.add(post)
    #         db.session.commit()
    #         post_title = Post.query.filter_by(title=post.title).first().title
    #         flash('Post "{}" created!'.format(post_title))
    #         return redirect(url_for('blog.home'))
    #
    # form = PostForm()
    #
    # return render_template(
    #     'new_post.html', form=form)
    pass


@blog.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    if request.method == 'POST':
        post_id = request.form['id']
        post = Post.query.filter_by(id=post_id).first()
        post.is_visible = False
        db.session.commit()
        flash('Post {} deleted!'.format(post_id))
        return redirect(url_for('blog.home'))


@blog.route('/new_comm/<int:post_id>', methods=['GET', 'POST'])
@login_required
def new_comm(post_id):
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        post = Post.query.filter_by(id=post_id).first()
        comment = Comment(user=user, post=post, text=request.form['text'])
        db.session.add(comment)
        db.session.commit()

        comments = Comment.query.filter_by(post_id=post_id)
        comments_json = {}
        for comm in comments:
            comments_json[comm.id] = {
                "content": comm.text,
                "date": str(comm.date)}
        return jsonify(comments_json)
        # TODO: must return comment.text, comment.id (for delete option)


@blog.route('/delete_comm', methods=['POST'])
@login_required
def delete_comm():
    if request.method == 'POST':
        comm_id = request.form['id']
        comment = Comment.query.filter_by(id=comm_id).first()
        comment.is_visible = False
        db.session.commit()
        flash('Comment {} deleted!'.format(comm_id))
        return redirect(url_for('blog.home'))


@blog.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'GET':
        return render_template('user_profile.html', form=BackwardForm())

    if request.method == 'POST':
        form = BackwardForm(request.form)
        if form.validate():
            msg = Message(
                form.title.data,
                sender=[current_user.username, 'flask.mail@yandex.ru'],
                recipients=['flask.mail@yandex.ru']
            )
            msg.body = form.text.data
            mail.send(msg)

            flash('Message will be send!')

        return redirect(url_for('blog.user_profile'))
