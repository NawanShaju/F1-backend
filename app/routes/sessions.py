from flask import Blueprint, request
from app.models.sessions_model import get_sessions_for_meeting
from app.utils.response_helper import create_response

bp = Blueprint('sessions', __name__)

@bp.get('/')
def all_sessions():
    meeting_key = request.args.get('meeting_key')
    result, msg = get_sessions_for_meeting(meeting_key)
    return create_response(result, msg)