from flask import flash, redirect, render_template, url_for, request

from market import app, db
from market.forms import AddItemForm, LoginForm, PurchaseItemForm, RegisterForm
from market.models import Item, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    print("it's a POST request")
    if purchase_form.validate_on_submit():
        item_to_be_purchased: Item = Item.query.filter_by(
            name=request.form.get('purchase_item_name')).first()
        if current_user.budget >= item_to_be_purchased.price:
            previous_owner: User = item_to_be_purchased.owned_user
            previous_owner.budget += item_to_be_purchased.price
            current_user.budget -= item_to_be_purchased.price
            item_to_be_purchased.owner = current_user.id
            db.session.commit()
        else:
            flash(f"unable to purchase item because of low budget",
                  category='danger')

    items = Item.query.all()
    items_owned_by_user = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items, items_owned_by_user=items_owned_by_user, purchase_form=purchase_form)


@ app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(
            f"Accont created for user {user_to_create.username} and Successfully logged in", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for fieldName, error_msg in form.errors.items():
            flash(
                f'There was an error in creating user in field - {form[fieldName].label.text} {error_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    # does two task validate and click on submit.
    if form.validate_on_submit():
        attempted_user: User = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user:
            if attempted_user.check_password_correction(
                attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(
                    f"Successfully logged in!! as user {attempted_user.username}", category='success')
                return redirect(url_for('market_page'))
            else:
                flash(
                    'Username and password are not matched!! Please try again', category='danger')
        else:
            flash(
                'Username not found in database', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Successfully logged out", category='info')
    return redirect(url_for('home_page'))


@app.route('/additem', methods=['POST', 'GET'])
def additem_page():
    form = AddItemForm()
    if form.validate_on_submit():
        item_to_create = Item(name=form.item_name.data,
                              price=form.price.data,
                              barcode=form.barcode.data,
                              description=form.description.data)
        item_to_create.owner = current_user.id
        db.session.add(item_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for fieldName, error_msg in form.errors.items():
            flash(
                f'There was an error in creating Item error in field - {form[fieldName].label.text} {error_msg}',
                category='danger')
    return render_template('add_item.html', form=form)
