import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	"""A simple class for the restaurants in the database"""
	
	__tablename__ = 'restaurant'

	name = Column(String(80), nullable = False)
	restaurant_id = Column(Integer, primary_key = True)


class MenuItem(Base):
	"""A class containing information about menu items in the restaurants"""
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable = False)
	item_id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		#Returns object in easily serializeable format
	    return {
	    	'name' : self.name,
	    	'description': self.description,
	    	'id': self.item_id,
	    	'price': self.price,
	    	'course': self.course
	    }


#  End
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)