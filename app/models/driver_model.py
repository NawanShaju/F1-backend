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
    
def get_driver_race_wins_in_year(driver_number: int, year: int = 2025):
    try:
        with F1DataManager(Config.DB_CONFIG) as manager:
            query = """
                SELECT 
                    s.circuit_short_name,
                    s.location,
                    d.driver_number,
                    d.full_name,
                    d.team_name,
                    s.date_start as win_dates
                FROM session_result sr
                JOIN drivers d
                    ON d.driver_number = sr.driver_number
                    AND d.session_key = sr.session_key
                JOIN sessions s
                    ON sr.session_key = s.session_key
                WHERE d.driver_number = %s
                    AND s.year = %s
                    AND sr.position = 1
                    AND s.session_name = 'Race'
                ORDER BY win_dates, s.circuit_short_name;
            """
                    
            return read_sql_query(query, manager.conn, params=(driver_number, year)).to_dict(orient='records'), "Data successfully retrived"
    except Exception as e:
        logger.error(f"Error fetching driver wins by year {year}: {e}")
        return None, e

def get_driver_podiums_in_year(driver_number: int, year: int = 2025):
    try:
        with F1DataManager(Config.DB_CONFIG) as manager:
            query = """
                SELECT 
                    s.circuit_short_name,
                    s.location,
                    d.driver_number,
                    d.full_name,
                    d.team_name,
                    s.date_start as win_dates
                FROM session_result sr
                JOIN drivers d
                    ON d.driver_number = sr.driver_number
                    AND d.session_key = sr.session_key
                JOIN sessions s
                    ON sr.session_key = s.session_key
                WHERE d.driver_number = %s
                    AND s.year = %s
                    AND sr.position <= 3
                    AND s.session_name = 'Race'
                ORDER BY win_dates, s.circuit_short_name;
            """
                    
            return read_sql_query(query, manager.conn, params=(driver_number, year)).to_dict(orient='records'), "Data successfully retrived"
    except Exception as e:
        logger.error(f"Error fetching driver wins by year {year}: {e}")
        return None, e