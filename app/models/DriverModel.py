from app.models.Query import Query

class DriverModel(Query):
    def __init__(self):
        super().__init__()

    def get_drivers_by_year(self, year: int = 2025):
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
        
        return self.query_db(query, (year,))
        
    def get_driver_race_wins_in_year(self, driver_number: int, year: int = 2025):
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
        return self.query_db(query, (driver_number, year))     
            

    def get_driver_podiums_in_year(self, driver_number: int, year: int = 2025):
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
        return self.query_db(query, (driver_number, year))