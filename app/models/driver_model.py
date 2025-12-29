import logging
from pandas import read_sql_query
from app.config import Config
from app.services.data_manager import F1DataManager

logger = logging.getLogger(__name__)

def get_drivers_by_year(year: int = 2025):
    try:
        with F1DataManager(Config.DB_CONFIG) as manager:
            query = """
                SELECT DISTINCT ON (d.driver_number)
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
                    
            return read_sql_query(query, manager.conn, params=(year,)).to_dict(orient='records'), "Data successfully retrived"
    except Exception as e:
        logger.error(f"Error fetching driver by year {year}: {e}")
        return None, e