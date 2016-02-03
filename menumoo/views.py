from flask import render_template, request, redirect, url_for
from menumoo import app, db

from .models import Restaurant, MenuItem


#  This view shows all restaurants, allowing you to navigate to their
#  specific menus as well as edit or delete restaurants
@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    restaurants = db.session.query(Restaurant).all()
    return render_template('restaurants.html',
        restaurants=restaurants)


#  This function returns a page to create a new restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name = request.form['name']
        restaurant = Restaurant(name=name)
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('newrestaurant.html')


#  This function returns a page for editing a restaurant's information
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
            db.session.add(restaurant)
            db.session.commit()
            return redirect(url_for('allRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    return render_template('deleterestaurant.html', restaurant=restaurant)

#  This function queries the database for the items of the restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    return render_template('menu.html', restaurant=restaurant, items=items)

#  Route for newMenuItem function
@app.route('/restaurants/<int:restaurant_id>/new/')
@app.route('/restaurants/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    return render_template('newmenuitem.html', restaurant=restaurant,
                           item=item)


#  Route for editMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit/')
def editMenuItem(restaurant_id, MenuID):
    return render_template('editmenuitem.html', restaurant=restaurant,
                           item=item)
#  Route for deleteMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/')
def deleteMenuItem(restaurant_id, MenuID):
    return render_template('deletemenuitem.html', restaurant=restaurant,
                           item=item)
