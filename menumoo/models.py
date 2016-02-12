from menumoo import db

class Restaurant(db.Model):
    """A simple class for the restaurants in the database"""
    
    __tablename__ = 'restaurant'

    name = db.Column(db.String(80), nullable = False)
    restaurant_id = db.Column(db.Integer, primary_key = True)

    #  This function as a property returns the data in an easily 
    #  serializeable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'restaurant_id': self.restaurant_id
        }
    

class MenuItem(db.Model):
    """A class containing information about menu items in the restaurants"""

    __tablename__ = 'menu_item'

    name = db.Column(db.String(80), nullable = False)
    item_id = db.Column(db.Integer, primary_key = True)
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
                              'restaurant.restaurant_id'))
    restaurant = db.relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'item_id': self.item_id,
            'course': self.course,
            'description': self.description,
            'price': self.price,
            'restaurant_id': self.restaurant_id
        }
