import logging
from pandas import read_sql_query
from app.config import Config
from app.services.data_manager import F1DataManager

logger = logging.getLogger(__name__)

def get_sessions_for_meeting(meetings: int):
    try:
        with F1DataManager(Config.DB_CONFIG) as manager:
            query = """
            SELECT DISTINCT ON (s.date_start)
            s.session_key,
            s.circuit_short_name,
            s.date_start,
            s.date_end,
            s.location,
            s.session_name,
            s.session_type
            FROM sessions s
            WHERE s.meeting_key = %s
            ORDER BY s.date_start;
            """
            return read_sql_query(query, manager.conn, params=(meetings,)).to_dict(orient='records'), "Data successfully retrived"
    except Exception as e:
        logger.error(f"Error fetching driver by year {meetings}: {e}")
        return None, e