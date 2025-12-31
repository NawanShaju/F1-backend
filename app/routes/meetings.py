from flask import Blueprint, request
from app.models.MeetingsModel import MeetingsModel
from app.utils.response_helper import create_response

bp = Blueprint('meetings', __name__, url_prefix='/meetings')
meetings_mode = MeetingsModel()

@bp.get('/')
def meetings_by_year():
    year = request.args.get('year', default=2025, type=int)
    df, msg = meetings_mode.get_meetings_by_year(year)
    result = df.to_dict(orient='records')
    return create_response(result, msg)

@bp.get('/get-meeting')
def meeting_by_key():
    meeting_key = request.args.get('meeting_key', default=2025, type=int)
    df, msg = meetings_mode.get_meeting_by_key(meeting_key)
    result = df.to_dict(orient='records')
    return create_response(result, msg)