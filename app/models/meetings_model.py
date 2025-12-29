import logging
from pandas import read_sql_query
from app.config import Config
from app.services.data_manager import F1DataManager

logger = logging.getLogger(__name__)

def get_meetings_by_year(year: int = 2025):
    try:
        with F1DataManager(Config.DB_CONFIG) as manager:
            query = """
            SELECT DISTINCT ON (m.date_start)
            m.meeting_key,
            m.country_code,
            m.country_name,
            m.date_start,
            m.location,
            m.meeting_name
            FROM meetings m
            WHERE m.year = %s
            ORDER BY m.date_start;
            """
            return read_sql_query(query, manager.conn, params=(year,)).to_dict(orient='records'), "Data successfully retrived"
    except Exception as e:
        logger.error(f"Error fetching driver by year {year}: {e}")
        return None, e