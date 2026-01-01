from app.models.Query import Query

class DbValidator(Query):
    def __init__(self):
        super().__init__()
        
    def exists_check(self, result, msg):
        if msg:
            return False
        elif len(result) == 0:
            return False
        
        return True
        
    def driver_exists_in_year(self, driver_number: int, year: int) -> bool:
        query = """
        SELECT DISTINCT ON (d.driver_number)
        d.full_name
        FROM Drivers d
        JOIN Sessions s
            ON s.session_key = d.session_key
        WHERE d.driver_number = %s AND s.year = %s
        """
        
        result, msg = self.query_db(query, (driver_number, year))
        return self.exists_check(result, msg)
    
    def driver_exists_in_session(self, driver_number: int, session: int) -> bool:
        query = """
        SELECT DISTINCT ON (d.driver_number)
        d.full_name
        FROM Drivers d
        WHERE d.driver_number = %s AND d.session_key = %s
        """
        
        result, msg = self.query_db(query, (driver_number, session))
        return self.exists_check(result, msg)

    def session_exists(self, session: int) -> bool:
        query = """
        SELECT session_key
        FROM sessions
        WHERE session_key = %s
        """
        
        result, msg = self.query_db(query, (session,))
        return self.exists_check(result, msg)