from menumoo import db


class User(db.Model):
    """This class contains information about the users of MenuMoo"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    picture = db.Column(db.String)

    #  This function as a property returns the data in an easily
    #  serializeable format
    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Restaurant(db.Model):
    """A simple class for the restaurants in the database"""

    __tablename__ = 'restaurant'

    restaurant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'restaurant_id': self.restaurant_id,
            'user_id': self.user_id
        }


class MenuItem(db.Model):
    """A class containing information about menu items in the restaurants"""

    __tablename__ = 'menu_item'

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
                              'restaurant.restaurant_id'))
    restaurant = db.relationship(Restaurant)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'item_id': self.item_id,
            'course': self.course,
            'description': self.description,
            'price': self.price,
            'restaurant_id': self.restaurant_id,
            'user_id': self.user_id
        }
