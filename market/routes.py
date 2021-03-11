from flask import flash, redirect, render_template, url_for

from market import app, db
from market.forms import LoginForm, RegisterForm
from market.models import Item, User
from flask_login import login_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(
                f'there was an error in creating user {error_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    # does two task validate and click on submit.
    if form.validate_on_submit():
        attempted_user: User = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Successfully logged in!! as user {attempted_user.username}", category='success')
            return redirect(url_for('market_page'))
        else:
            flash(
                'Username and password are not matched!! Please try again', category='danger')

    return render_template('login.html', form=form)
