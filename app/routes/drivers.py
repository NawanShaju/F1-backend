from flask import Blueprint, jsonify, make_response, request
from app.models.driver_model import get_drivers_by_year
from app.utils.response_helper import create_response

bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@bp.get('/')
def drivers_by_year():
    year = request.args.get('year')
    result, msg = get_drivers_by_year(year)
    return create_response(result, msg)