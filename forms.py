from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class CheckoutForm(FlaskForm):
    name = StringField('Ism', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Manzil', validators=[DataRequired(), Length(min=5)])

