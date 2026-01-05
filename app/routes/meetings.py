from flask import Blueprint, request, jsonify, make_response
from app.models.MeetingsModel import MeetingsModel
from app.utils.response_helper import create_response
from app.services.circuit_scraper import scrap_circuit_info
from app.utils.DbValidator import DbValidator

bp = Blueprint('meetings', __name__, url_prefix='/meetings')
meetings_mode = MeetingsModel()
validator = DbValidator()

@bp.get('/')
def meetings_by_year():
    year = request.args.get('year', default=2025, type=int)
    df, msg = meetings_mode.get_meetings_by_year(year)
    result = df.to_dict(orient='records')
    return create_response(result, msg)

@bp.get('/get-meeting')
def meeting_by_key():
    meeting_key = request.args.get('meeting_key', type=int)
    
    if not validator.meeting_exists(meeting_key):
        return make_response(jsonify({'error': f'The meeting with key {meeting_key} does not exists'}), 404)
    
    df, msg = meetings_mode.get_meeting_by_key(meeting_key)
    result = df.to_dict(orient='records')
    return create_response(result, msg)

@bp.get('/get-meeting-info')
def meeting_info():
    meeting_key = request.args.get('meeting_key', type=int)
    
    if not validator.meeting_exists(meeting_key):
        return make_response(jsonify({'error': f'The meeting with key {meeting_key} does not exists'}), 404)
    
    df, msg = meetings_mode.get_meeting_by_key(meeting_key)
        
    country_name = df.iloc[0]["country_name"]
    year = df.iloc[0]["year"]
    
    if country_name is None or year is None:
        return create_response(None, "The session or the year does not exists")
    
    result = scrap_circuit_info(str(year), str(country_name))
    
    if not isinstance(result, dict):
        return create_response(None, f"The information for the circuit in {country_name} for the year {year} is not available")
    
    return create_response(result, None)