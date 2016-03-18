from flask import render_template, request, redirect, url_for, jsonify, flash
from menumoo import app, db

from .models import Restaurant, MenuItem, User
from .forms import NameForm, MenuItemForm

#  Security
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


#  Helper functions for info about users
def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.user_id
    except:
        return None


def getUserInfo(user_id):
    user = db.session.query(User).filter_by(user_id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'], email=
        login_session['email'], picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.user_id


#  Create a state token to prevent request forgery.
#  Store it in the session for later validation.
#  Send state through to the jinja template
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/fbconnect', methods=['GET', 'POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps("Invalid state parameter"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    #  Exchange the access token for a long lived server-side token for server
    #  to server API calls.
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    #  Strip expire tag from access token
    token = result.split('&')[0]

    #  Save the access token to be able to revoke fb permissions on disconnect
    login_session['provider'] = 'facebook'
    login_session['access_token'] = token

    #  Use token to get user info from API
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    #  Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=300&width=300' % token
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data['data']['url']
    
    #  See if the user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "You have been logged out."


#  Load the google client id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


#  This method exchanges the one time auth code sent by google to the client
#  side.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    print request.args.get('state')
    print login_session['state']
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
        response = make_response(json.dumps('Failed to Upgrade the\
                                            authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    #  Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match\
                                            given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match\
                                            app's."))
        response.headers['Content-Type'] = 'application/json'
        return response

    #  Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already\
                                            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    #  Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #  Get user info
    userinfo_url = "https://www.googleapis.com/userinfo/v2/me"
    parameters = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=parameters)
    data = json.loads(answer.text)
    print data

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]


    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    return output


#  DISCONNECT - Revoke a current user's token and reset their login_session.
@app.route("/gdisconnect")
def gdisconnect():
    #  Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #  Execute HTTP GET request to revoke the current token.
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        #  For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['access_token']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash('You have been successfully logged out.')
        return redirect(url_for('allRestaurants'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('allRestaurants'))



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

    if 'username' not in login_session:
        return render_template('publicrestaurants.html',
                               restaurants=restaurants)        
    else:
        return render_template('restaurants.html',
                               restaurants=restaurants,
                               form=form)


#  This function returns a form to create a new restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/login')

    form = NameForm()

    if form.validate_on_submit():
        name = form.data['name']
        description = form.data['description']
        restaurant = Restaurant(name=name,
        						description=description,
        						user_id=login_session['user_id'])
        db.session.add(restaurant)
        db.session.commit()
        flash("New restaurant has been created!")
        return redirect(url_for('allRestaurants'))
    return render_template('newrestaurant.html', form=form)


#  This function returns a page for editing a restaurant's information
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')

    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()

    if login_session['user_id'] != restaurant.user_id:
    	return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"

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
    if 'username' not in login_session:
        return redirect('/login')

    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()

    if login_session['user_id'] != restaurant.user_id:
	    return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()'>"


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
    creator = getUserInfo(restaurant.user_id)

    if 'username' not in login_session or creator.user_id != login_session['user_id']:
        return render_template('publicmenu.html',
        					   restaurant=restaurant,
        					   items=items,
        					   creator=creator)        
    else:
        return render_template('menu.html',
        					   restaurant=restaurant,
        					   items=items,
        					   creator=creator)


#  Route for newMenuItem function
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
@app.route('/restaurants/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')

    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()

    if login_session['user_id'] != restaurant.user_id:
    	return "<script>function myFunction() {alert('You are not authorized to create a new item for this restaurant. Please create your own restaurant in order to create items.');}</script><body onload='myFunction()'>"

    form = MenuItemForm()

    if form.validate_on_submit():
        item = MenuItem(name=form.data['name'],
                        description=form.data['description'],
                        course=form.data['course'],
                        price=form.data['price'],
                        restaurant_id=restaurant_id, 
                        user_id=login_session['user_id'])
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
    if 'username' not in login_session:
        return redirect('/login')

    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    item = db.session.query(MenuItem).filter_by(item_id=MenuID).one()

    if login_session['user_id'] != item.user_id:
    	return "<script>function myFunction() {alert('You are not authorized to edit this menu item. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"

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
    if 'username' not in login_session:
        return redirect('/login')
    
    restaurant = db.session.query(Restaurant).filter_by(
        restaurant_id=restaurant_id).one()
    item = db.session.query(MenuItem).filter_by(item_id=MenuID).one()

    if login_session['user_id'] != item.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this menu item. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()'>"

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
