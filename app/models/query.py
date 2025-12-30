import logging
from pandas import read_sql_query
from app.config import Config
from psycopg2 import connect
from typing import Optional, Tuple, List, Dict, Any

class Query:
    """Base class for database queries with connection management"""
    
    def __init__(self):
        self.conn = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        if not self.conn or self.conn.closed:
            self.conn = connect(**Config.DB_CONFIG)
            self.logger.info("Database connection established")
    
    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.logger.info("Database connection closed")
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def query_db(self, query: str, params: Optional[Tuple] = None) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Execute a query and return results as list of dicts
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            
        Returns:
            Tuple of (results, message) or (None, error_message)
        """
        try:
            if not self.conn or self.conn.closed:
                self.connect()
            
            df = read_sql_query(query, self.conn, params=params)
            result = df.to_dict(orient='records')
            return result, None
            
        except Exception as e:
            self.logger.error(f"Error fetching data from database: {e}")
            return None, str(e)