from flask import Blueprint, jsonify, make_response, request
from app.models.driver_model import get_drivers_by_year, get_driver_race_wins_in_year, get_driver_podiums_in_year
from app.utils.response_helper import create_response

bp = Blueprint('drivers', __name__, url_prefix='/drivers')

@bp.get('/')
def drivers_by_year():
    year = request.args.get('year')
    result, msg = get_drivers_by_year(year)
    return create_response(result, msg)

@bp.get('/race-wins')
def driver_race_win_by_year():
    driver_number = request.args.get('driver_number')
    year = request.args.get('year')
    result, msg = get_driver_race_wins_in_year(driver_number, year)
    
    if len(result) == 0:
        return make_response(jsonify({'info': f'Driver did not win in the year {year}'}), 200)
    
    return create_response(result, msg)

@bp.get('/podiums')
def driver_podiums_by_year():
    driver_number = request.args.get('driver_number')
    year = request.args.get('year')
    result, msg = get_driver_podiums_in_year(driver_number, year)
    
    if len(result) == 0:
        return make_response(jsonify({'info': f'Driver did not get podiums in the year {year}'}), 200)
    
    return create_response(result, msg)