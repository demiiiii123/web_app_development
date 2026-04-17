from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
lobby_bp = Blueprint('lobby', __name__)
game_bp = Blueprint('game', __name__)

from . import auth_routes, lobby_routes, game_routes, socket_events
