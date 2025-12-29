from flask import Blueprint, request
from app.models.session_result_model import get_session_result_for_session
from app.utils.response_helper import create_response

bp = Blueprint('session_result', __name__)

@bp.get('/')
def all_sessions():
    session_key = request.args.get('session_key')
    result, msg = get_session_result_for_session(session_key)
    return create_response(result, msg)