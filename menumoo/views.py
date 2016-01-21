from flask import render_template, request
from menumoo import app


#  This view shows all restaurants, allowing you to navigate to their
#  specific menus as well as edit or delete restaurants
@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    return "This page shows all the restaurants."


#  This function returns a page to create a new restaurant
@app.route('/restaurants/new/')
def newRestaurant():
    return "This page shows a form for creating a new restaurant."


# This function returns a page for editing a restaurant's information
@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return "This page edits a restaurant's information."


# This function returns a page confirming deletion of a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return "This page confirms the deletion of a restaurant."


# This function queries the database for the items of the restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    pass

# Route for newMenuItem function
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    pass


# Route for editMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    pass


# Route for deleteMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, MenuID):
    pass