from flask import render_template, request, redirect, url_for, jsonify
from menumoo import app, db

from .models import Restaurant, MenuItem

#  JSON API endpoint for all restaurants
@app.route('/JSON/')
@app.route('/restaurants/JSON/')
def allRestaurantsJSON():
    restaurants = db.session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])

#  JSON API endpoint for a restaurant with ID
@app.route('/restaurants/<int:restaurant_id>/JSON/')
def restaurantJSON():
    pass


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
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        db.session.delete(restaurant)
        db.session.commit()
        return redirect(url_for("allRestaurants"))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurant)


#  This function queries the database for the items of the restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


#  Route for newMenuItem function
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        item = MenuItem(name=request.form['name'],
                        description=request.form['description'],
                        course=request.form['course'],
                        price=request.form['price'],
                        restaurant_id=restaurant_id
                        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant=restaurant)


#  Route for editMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
    item = db.session.query(MenuItem).filter_by(item_id=MenuID).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['course']:
            item.course = request.form['course']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant=restaurant,
                           item=item)


#  Route for deleteMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, MenuID):
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()
    item = db.session.query(MenuItem).filter_by(item_id=MenuID).one()
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant=restaurant,
                           item=item)
