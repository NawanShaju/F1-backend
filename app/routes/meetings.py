from flask import Blueprint, request
from app.models.MeetingsModel import MeetingsModel
from app.utils.response_helper import create_response

bp = Blueprint('meetings', __name__, url_prefix='/meetings')


@bp.get('/')
def meetings_by_year():
    """Get all meetings for a specific year"""
    year = request.args.get('year', default=2025, type=int)
    
    with MeetingsModel() as model:
        result, msg = model.get_meetings_by_year(year)
    
    return create_response(result, msg)


@bp.get('/get-meeting')
def meeting_by_key():
    """Get specific meeting details"""
    meeting_key = request.args.get('meeting_key', default=2025, type=int)
    
    with MeetingsModel() as model:
        result, msg = model.get_meeting_by_key(meeting_key)
    
    return create_response(result, msg)