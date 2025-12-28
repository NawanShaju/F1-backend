from flask import Blueprint, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

bp = Blueprint('drivers', __name__, url_prefix='/driver')

@bp.get('/')
def driverHome():
    return jsonify({'test': "tester"})


def get_drivers_by_year(conn, year: int):

    query = """
        SELECT DISTINCT
            d.id,
            d.driver_number,
            d.first_name,
            d.last_name,
            d.full_name,
            d.broadcast_name,
            d.name_acronym,
            d.team_name,
            d.team_colour,
            d.country_code,
            d.headshot_url
        FROM drivers d
        JOIN sessions s
            ON d.session_key = s.session_key
        WHERE s.year = %s
        ORDER BY d.driver_number;
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (year,))
        return cursor.fetchall()