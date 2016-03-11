from flask import render_template, request, redirect, url_for, jsonify, flash
from menumoo import app, db

from .models import Restaurant, MenuItem
from .forms import NameForm, MenuItemForm

#  Security
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

#  Create a state token to prevent request forgery.
#  Store it in the session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    code = request.data

    try:
        #  Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to Upgrade th authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/outh2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    #  Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."))
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'


#  This view shows all restaurants, allowing you to navigate to their
#  specific menus as well as edit or delete restaurants
@app.route('/')
@app.route('/restaurants/', methods=['GET', 'POST'])
def allRestaurants():
    restaurants = db.session.query(Restaurant).all()
    form = NameForm()

    if form.validate_on_submit():
        name = form.data['name']
        description = form.data['description']
        restaurant = Restaurant(name=name, description=description)
        db.session.add(restaurant)
        db.session.commit()
        flash("New restaurant has been created!")
        return redirect(url_for('allRestaurants'))
    return render_template('restaurants.html',
                           restaurants=restaurants,
                           form=form)


#  This function returns a form to create a new restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    form = NameForm()

    if form.validate_on_submit():
        name = form.data['name']
        description = form.data['description']
        restaurant = Restaurant(name=name, description=description)
        db.session.add(restaurant)
        db.session.commit()
        flash("New restaurant has been created!")
        return redirect(url_for('allRestaurants'))
    return render_template('newrestaurant.html', form=form)


#  This function returns a page for editing a restaurant's information
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    form = NameForm(obj=restaurant)

    if form.validate_on_submit():
        form.populate_obj(restaurant)
        db.session.add(restaurant)
        db.session.commit()
        flash("Restaurant edits have been saved!")
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('editrestaurant.html',
                               restaurant=restaurant,
                               form=form)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        db.session.delete(restaurant)
        db.session.commit()
        flash("The restaurant has been deleted!")
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurant)


#  This function queries the database for the items of the restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    items = db.session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


#  Route for newMenuItem function
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    form = MenuItemForm()

    if form.validate_on_submit():
        item = MenuItem(name=form.data['name'],
                        description=form.data['description'],
                        course=form.data['course'],
                        price=form.data['price'],
                        restaurant_id=restaurant_id)
        db.session.add(item)
        db.session.commit()
        flash("New menu item has been created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',
                               restaurant=restaurant,
                               form=form)


#  Route for editMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    item = db.session.query(MenuItem).filter_by(item_id=MenuID).one()
    form = MenuItemForm(obj=item)

    if request.method == 'POST' and form.validate():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Menu item has been edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',
                               restaurant=restaurant,
                               item=item,
                               form=form)


#  Route for deleteMenuItem function
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, MenuID):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    item = db.session.query(MenuItem).filter_by(item_id=MenuID).one()
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("Menu item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant=restaurant,
                               item=item)


#  JSON API endpoint for all restaurants
@app.route('/JSON/')
@app.route('/restaurants/JSON/')
def allRestaurantsJSON():
    restaurants = db.session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


#  JSON API endpoint for a particular restaurant
@app.route('/restaurants/<int:restaurant_id>/JSON/')
def restaurantJSON(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    return jsonify(Restaurant=restaurant.serialize)


#  JSON API endpoint for a restaurant's menu
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def menuJSON(restaurant_id):
    items = db.session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


#  JSON API endpoint for a particular menu item
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/JSON')
def menuItemJSON(restaurant_id, MenuID):
    item = db.session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, item_id=MenuID).one()
    return jsonify(MenuItem=item.serialize)
