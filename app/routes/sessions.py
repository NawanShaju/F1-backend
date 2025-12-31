from flask import Blueprint, request
from app.models.SessionsModel import SessionsModel
from app.utils.response_helper import create_response

bp = Blueprint('sessions', __name__)
sessons_model = SessionsModel()

@bp.get('/')
def all_sessions():
    meeting_key = request.args.get('meeting_key')
    df, msg = sessons_model.get_sessions_for_meeting(meeting_key)
    result = df.to_dict(orient='records')
    return create_response(result, msg)

@bp.get('/get-session')
def meeting_by_key():
    session_key = request.args.get('session_key')
    df, msg = sessons_model.get_session_by_key(session_key)
    result = df.to_dict(orient='records')
    return create_response(result, msg)