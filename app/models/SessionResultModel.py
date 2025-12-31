from app.models.Query import Query

class SessionResultModel(Query):
    def __init__(self):
        super().__init__()
    
    def get_session_result_for_session(self, session_key):
        query = """
        SELECT DISTINCT ON (sr.position, sr.driver_number)
        sr.position,
        sr.number_of_laps,
        sr.gap_to_leader,
        sr.duration,
        sr.driver_number,
        d.full_name,
        d.team_name,
        d.team_colour,
        sr.dnf,
        sr.dns,
        sr.dsq,
        sr.points,
        d.headshot_url
        FROM session_result sr
        JOIN drivers d
                ON d.driver_number = sr.driver_number
        WHERE sr.session_key = %s
        ORDER BY sr.position, sr.driver_number;
        """
        
        return self.query_db(query, (session_key,))