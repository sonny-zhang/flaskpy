"""Create the auth blueprint, introduce routing from views.py module"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
