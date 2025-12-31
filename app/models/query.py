import logging
from pandas import read_sql_query
from app.config import Config
from psycopg2 import connect
from typing import Optional, Tuple, List, Dict, Any

class Query:
    """Base class for database queries with connection management"""
    
    def __init__(self):
        self.conn_string = Config.DATABASE_URL
        self.logger = logging.getLogger(__name__)
        
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
            df = read_sql_query(query, self.conn_string, params=params)
            return df, None
            
        except Exception as e:
            self.logger.error(f"Error fetching data from database: {e}")
            return None, str(e)