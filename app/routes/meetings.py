from flask import Blueprint, request
from app.models.meetings_model import get_meetings_by_year
from app.utils.response_helper import create_response

bp = Blueprint('meetings', __name__, url_prefix='/meetings')

@bp.get('/')
def meetings_by_year():
    year = request.args.get('year')
    result, msg = get_meetings_by_year(year)
    return create_response(result, msg)