#  forms.py
#  For learning the use of WTForms

from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField
from wtforms.validators import DataRequired


class NameForm(Form):
	"""docstring for NameForm"""
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])


class MenuItemForm(Form):
	"""docstring for NameForm"""
	name = StringField('Name', validators=[DataRequired()])
	course = RadioField('Course', choices=['Appetizer', 'Entree', 'Side', 'Dessert'])
	price = DecimalField('Price', places=2)
	description = StringField('Name', validators=[DataRequired()])
