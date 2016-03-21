{% extends "layout.html" %}
{% block nav %}
<li><a href="{{ url_for('allRestaurants') }}">All Restaurants</a></li>
<li><a href="{{ url_for('newRestaurant') }}">New Restaurant</a></li>
{% endblock %}
{% block spiel %}
<div class="container spiel">
    <div class="six columns offset-by-three box">
        <h2>An easier way to keep track of your favorite restaurants</h2>
        <p>This Flask application is powered by SQLAlchemy and numerous Flask
            extensions, such as flask-wtforms.</p>

            <form action="{{ url_for('newRestaurant') }}" method="POST">
                {{ form.hidden_tag() }}
                {{ form.name(size=20, placeholder=form.name.label.text) }}
                {{ form.description(size=25, placeholder=form.description.label.text) }}
                {{ form.picture(size=25, placeholder=form.picture.label.text) }}

                <input type="submit" class="button-primary" value="Create Restaurant">
            </form>

        </div>
    </div> <!-- Container -->
    {% endblock %}

    {% block heading %}Restaurants{% endblock %}
    {% block content %}

    {% if restaurants %}

    {% for restaurant in restaurants %}

    <div class="box">
        <h4><a href="{{ url_for('restaurantMenu', restaurant_id=restaurant.restaurant_id) }}">{{ restaurant.name }}</a></h4>
        <p>{{ restaurant.description }}</p>
        <img src="{{ restaurant.picture }}">
        <div class="crud">            
            <a href="{{ url_for('editRestaurant', restaurant_id=restaurant.restaurant_id) }}">Edit</a>
            <a href="{{ url_for('deleteRestaurant', restaurant_id=restaurant.restaurant_id) }}">Delete</a>
        </div>          
    </div>

    {% endfor %}

    {% else %}
    <div class="box">
        <h4>No Restaurants</h4>
        <p>There are currently no restraurants in the database. Use the link above to add some!</p>
    </div>
    {% endif %}
    {% endblock %}