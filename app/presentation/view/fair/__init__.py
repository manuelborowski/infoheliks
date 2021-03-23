from flask import Blueprint

fair = Blueprint('fair', __name__)

from . import views
