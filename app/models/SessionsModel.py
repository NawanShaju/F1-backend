from app.models.Query import Query

class SessionsModel(Query):
    
    def __init__(self):
        super().__init__()

    def get_sessions_for_meeting(self, meeting_key: int):
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
        
        return self.query_db(query, (meeting_key,))