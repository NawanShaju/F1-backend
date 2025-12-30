from flask import Blueprint, request
from app.models.SessionsModel import SessionsModel
from app.utils.response_helper import create_response

bp = Blueprint('sessions', __name__)
sessons_model = SessionsModel()

@bp.get('/')
def all_sessions():
    meeting_key = request.args.get('meeting_key')
    result, msg = sessons_model.get_sessions_for_meeting(meeting_key)
    return create_response(result, msg)