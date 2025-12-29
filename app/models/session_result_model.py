import logging
from pandas import read_sql_query
from app.config import Config
from app.services.data_manager import F1DataManager

logger = logging.getLogger(__name__)

def get_session_result_for_session(session_key):
    try:
        with F1DataManager(Config.DB_CONFIG) as manager:
            query = """
            SELECT DISTINCT ON (sr.position, sr.driver_number)
            sr.position,
            sr.number_of_laps,
            sr.gap_to_leader,
            sr.driver_number,
            d.full_name,
            d.team_name,
            sr.dnf,
            sr.dns,
            sr.dsq,
            sr.points
            FROM session_result sr
            JOIN drivers d
                    ON d.driver_number = sr.driver_number
            WHERE sr.session_key = %s
            ORDER BY sr.position, sr.driver_number;
            """
            return read_sql_query(query, manager.conn, params=(session_key,)).to_dict(orient='records'), "Data successfully retrived"
    except Exception as e:
        logger.error(f"Error fetching result for session {session_key}: {e}")
        return None, e