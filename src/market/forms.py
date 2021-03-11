from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from market.models import User, Item


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'This Username already exists in the database, Please try another one!')

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError(
                'This Email already exists in the database, Please try another one!')

    username = StringField(label="User Name:", validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label="Email Address:", validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):

    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[
        DataRequired()])

    submit = SubmitField(label="Sign In")


class AddItemForm(FlaskForm):

    def validate_item_name(self, item_name_to_check):
        item = Item.query.filter_by(name=item_name_to_check.data).first()
        if item:
            raise ValidationError(
                'This Item already exists in the database, Please try another one!')

    item_name = StringField(label="Item Name:", validators=[
        Length(min=6, max=30), DataRequired()])
    price = IntegerField(label="Price:", validators=[DataRequired()])
    barcode = StringField(label="Bar Code", validators=[
                          Length(min=12, max=12), DataRequired()])
    description = StringField(label="Description", validators=[
                              DataRequired(), Length(min=4, max=1024)])

    submit = SubmitField(label="Add Item")
