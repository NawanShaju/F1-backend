from app.models.Query import Query

class Validator(Query):
    def __init__(self):
        super().__init__()
        
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
        
        if msg:
            return False
        elif len(result) == 0:
            return False
        
        return True