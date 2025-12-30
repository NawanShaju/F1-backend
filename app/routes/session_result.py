from flask import Blueprint, request
from app.models.SessionResultModel import SessionResultModel
from app.utils.response_helper import create_response

bp = Blueprint('session_result', __name__)
session_result_model = SessionResultModel()

@bp.get('/')
def all_sessions():
    session_key = request.args.get('session_key')
    result, msg = session_result_model.get_session_result_for_session(session_key)
    return create_response(result, msg)