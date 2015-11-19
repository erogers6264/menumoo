
import sys

from sqlalchemy import
Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import
declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	"""docstring for Restaurant"""
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

	def __init__(self, arg):
		super(Restaurant, self).__init__()
		self.arg = arg
		


class MenuItem(Base):
	"""docstring for MenuItem"""
	__tablename__ = 'menu_item'

	def __init__(self, arg):
		super(MenuItem, self).__init__()
		self.arg = arg
		


### END ###
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)