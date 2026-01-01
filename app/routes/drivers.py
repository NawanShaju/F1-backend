from flask import Blueprint, jsonify, make_response, request
from app.models.DriverModel import DriverModel
from app.utils.response_helper import create_response
from app.utils.DbValidator import DbValidator

bp = Blueprint('drivers', __name__, url_prefix='/drivers')
driver_model = DriverModel()
validatior = DbValidator()

@bp.get('/')
def drivers_by_year():
    year = request.args.get('year')
    df, msg = driver_model.get_drivers_by_year(year)
    result = df.to_dict(orient='records')
    return create_response(result, msg)

@bp.get('/driver')
def driver_by_number_and_session():
    session_key = request.args.get('session_key')
    
    if not validatior.session_exists(session_key):
        return make_response(jsonify({'error': f'The session {session_key} does not exist'}), 404)
    
    driver_number = request.args.get('driver_number')
    
    if not validatior.driver_exists_in_session(driver_number, session_key):
        return make_response(jsonify({'error': f'Driver with number {driver_number} does not exist in the session {session_key}'}), 404)
    
    
    df, msg = driver_model.get_driver_info(driver_number, session_key)
    result = df.to_dict(orient='records')
    return create_response(result, msg)

@bp.get('/race-wins')
def driver_race_win_by_year():
    driver_number = request.args.get('driver_number')
    year = request.args.get('year')
    
    if not validatior.driver_exists_in_year(driver_number, year):
        return make_response(jsonify({'error': f'Driver with number {driver_number} does not exist in the year {year}'}), 404)
    
    df, msg = driver_model.get_driver_race_wins_in_year(driver_number, year)
    result = df.to_dict(orient='records')
    
    if len(result) == 0:
        return make_response(jsonify({'info': f'Driver did not win in the year {year}'}), 200)
    
    return create_response(result, msg)

@bp.get('/podiums')
def driver_podiums_by_year():
    driver_number = request.args.get('driver_number')
    year = request.args.get('year')
    
    if not validatior.driver_exists_in_year(driver_number, year):
        return make_response(jsonify({'error': f'Driver with number {driver_number} does not exist in the year {year}'}), 404)
    
    df, msg = driver_model.get_driver_podiums_in_year(driver_number, year)
    result = df.to_dict(orient='records')
    
    if len(result) == 0:
        return make_response(jsonify({'info': f'Driver did not get podiums in the year {year}'}), 200)
    
    return create_response(result, msg)