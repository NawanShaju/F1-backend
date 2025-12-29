from flask import Blueprint, jsonify, make_response
from app.models.meetings_model import get_meetings_by_year
from app.models.sessions_model import get_sessions_for_meeting

bp = Blueprint('meetings', __name__, url_prefix='/meetings')

@bp.get('/<int:year>')
def meetings_by_year(year):
    result, msg = get_meetings_by_year(year)
    
    if result is None:
        response = make_response(jsonify({'error': msg}), 500)
        return response
    elif len(result) == 0:
        response = make_response(jsonify({'error': "Data not available"}), 404)
        return response
    
    response = make_response(jsonify(result), 200)
    return response

@bp.get('/sessions/<int:meeting_key>')
def all_sessions_for_meeting(meeting_key):
    result, msg = get_sessions_for_meeting(meeting_key)
    
    if result is None:
        response = make_response(jsonify({'error': msg}), 500)
        return response
    elif len(result) == 0:
        response = make_response(jsonify({'error': "Data not available"}), 404)
        return response
    
    response = make_response(jsonify(result), 200)
    return response