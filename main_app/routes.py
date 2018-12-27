import os
import secrets
from PIL import Image
from flask import (render_template, jsonify, url_for, flash, redirect, request)
from datetime import datetime
import json
from main_app import app, db, bcrypt
from main_app.forms import (LoginForm, RegistrationForm, RequestForm)
from main_app.models import User, ProductEnum, Client, Request
from flask_login import (login_user, current_user, logout_user, login_required)


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Requests'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Requests'))
        else:
            flash('You have previously unsuccessful login attempts', 'danger')
# <<<<<<< Updated upstream
# =======
            return redirect(url_for('login'))
# >>>>>>> Stashed changes
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('Requests'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/Requests", methods=['GET', 'POST'])
def Requests():
    clients=Client.query.all()
    request_form = RequestForm()
    if request.method == 'POST':
        if request_form.validate_on_submit():
            data = Request.query.filter(
                        Request.priority>=request_form.priority.data,
                        Request.client_id==request_form.client.data).all()
            for obj in data:
                obj.priority = obj.priority + 1
            priority = request_form.priority.data
            request_count = Request.query.filter(
                        Request.client_id==request_form.client.data).count()
            if priority >= request_count+1:
                priority = request_count + 1

            new_request = Request(
                    title=request_form.title.data,
                    description=request_form.description.data,
                    client_id=request_form.client.data,
                    priority=priority,
                    target_date=request_form.target_date.data,
                    product=request_form.product.data,
            )
            data.append(new_request)
            db.session.add_all(data)
            db.session.commit()
            flash('successful', 'success')
            return redirect(url_for('Requests'))
        else:
            flash('Oops!!! error', 'error')
    return render_template('feature_req.html', request_form=request_form, clients=clients)

@app.route('/getdata/')
def get_request_data():
    clients = [{"id":x.id, "name":x.name, "requests": x.request.count()} for x in Client.query.all()]
    products = [[x.name, x.name.capitalize()] for x in ProductEnum]
    return jsonify(clients=clients, products=products)
