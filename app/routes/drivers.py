from flask import Blueprint, jsonify, make_response, request
from app.models.driver_model import get_drivers_by_year

bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@bp.get('/')
def drivers_by_year():
    year = request.args.get('year')
    result, msg = get_drivers_by_year(year)
    
    if result is None:
        response = make_response(jsonify({'error': msg}), 500)
        return response
    elif len(result) == 0:
        response = make_response(jsonify({'error': "Data not available"}), 404)
        return response
    
    response = make_response(jsonify(result), 200)
    return response