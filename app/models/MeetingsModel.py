from app.models.Query import Query

class MeetingsModel(Query):
    """Model for meetings-related database operations"""
    
    def __init__(self):
        super().__init__()
    
    def get_meetings_by_year(self, year: int = 2025):
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
        
        return self.query_db(query, (year,))
    
    def get_meeting_by_key(self, meeting_key: int):
        query = """
            SELECT 
            m.circuit_short_name,
            m.country_code,
            m.country_name,
            m.date_start,
            m.location,
            m.meeting_name,
            m.meeting_official_name,
            m.year
            FROM meetings m
            WHERE meeting_key = %s;
        """
        
        result, error = self.query_db(query, (meeting_key,))
        
        print(result)
        
        if result and len(result) > 0:
            return result[0], None
        
        return None, error or "Meeting not found"