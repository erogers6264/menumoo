from flask import render_template, request
from menumoo import app


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


#  This view shows all restaurants, allowing you to navigate to their
#  specific menus as well as edit or delete restaurants
@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    return render_template('restaurants.html',
        restaurants=restaurants)


#  This function returns a page to create a new restaurant
@app.route('/restaurants/new/')
def newRestaurant():
    return render_template('newrestaurant.html',restaurant=restaurant)


# This function returns a page for editing a restaurant's information
@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return render_template('editrestaurant.html', restaurant=restaurant)


#  This function returns a page confirming deletion of a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/')
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