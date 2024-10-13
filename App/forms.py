from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TicketForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_date = DateTimeField('Event Date', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    available_tickets = IntegerField('Available Tickets', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Ticket')

class OrderForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Place Order')
