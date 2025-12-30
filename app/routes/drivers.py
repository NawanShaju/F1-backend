from flask import Blueprint, jsonify, make_response, request
from app.models.DriverModel import DriverModel
from app.utils.response_helper import create_response
from app.utils.Validator import Validator

bp = Blueprint('drivers', __name__, url_prefix='/drivers')
driver_model = DriverModel()
validatior = Validator()

@bp.get('/')
def drivers_by_year():
    year = request.args.get('year')
    result, msg = driver_model.get_drivers_by_year(year)
    return create_response(result, msg)

@bp.get('/race-wins')
def driver_race_win_by_year():
    driver_number = request.args.get('driver_number')
    year = request.args.get('year')
    
    if not validatior.driver_exists_in_year(driver_number, year):
        return make_response(jsonify({'error': f'Driver with number {driver_number} does not exist in the year {year}'}), 404)
    
    result, msg = driver_model.get_driver_race_wins_in_year(driver_number, year)
    
    if len(result) == 0:
        return make_response(jsonify({'info': f'Driver did not win in the year {year}'}), 200)
    
    return create_response(result, msg)

@bp.get('/podiums')
def driver_podiums_by_year():
    driver_number = request.args.get('driver_number')
    year = request.args.get('year')
    
    if not validatior.driver_exists_in_year(driver_number, year):
        return make_response(jsonify({'error': f'Driver with number {driver_number} does not exist in the year {year}'}), 404)
    
    result, msg = driver_model.get_driver_podiums_in_year(driver_number, year)
    
    if len(result) == 0:
        return make_response(jsonify({'info': f'Driver did not get podiums in the year {year}'}), 200)
    
    return create_response(result, msg)