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

from functools import wraps


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
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.user_id