#  forms.py
#  For learning the use of WTForms

from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField
from wtforms.validators import DataRequired


class NameForm(Form):
    """docstring for NameForm"""
    name = StringField('Restaurant Name', validators=[DataRequired(
                       "You need to provide a name.")])
    description = StringField('Description', validators=[DataRequired(
                              "You need to provide a description.")])


class MenuItemForm(Form):
    """docstring for MenuItemForm"""
    name = StringField('Item Name', validators=[DataRequired()])
    course = RadioField('Course', choices=[('Appetizer', 'Appetizer'),
                                           ('Entree', 'Entree'),
                                           ('Side', 'Side'),
                                           ('Beverage', 'Beverage'),                                 
                                           ('Dessert', 'Dessert')],
                        validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
