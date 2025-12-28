import psycopg2
from psycopg2.extras import execute_batch
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CacheConfig:
    """Configuration for what data to pre-load vs lazy-load"""
    priority_tables = [
        'meetings', 'sessions', 'drivers', 
        'laps', 'stints', 'pit', 'session_result', 
        'starting_grid', 'race_control', 'weather'
    ]
    lazy_tables = ['car_data', 'location', 'intervals', 'position']
    recent_sessions_count = 3  # Pre-load last N race weekends


class F1DataManager:
    """Manages F1 data with hybrid loading strategy"""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize the data manager
        
        Args:
            db_config: Dict with keys: host, database, user, password, port
        """
        self.db_config = db_config
        self.api_base_url = "https://api.openf1.org/v1"
        self.config = CacheConfig()
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(**self.db_config)
            logger.info("Database connection established")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    # ==================== API FETCHING ====================    
    """
    Fetch data from OpenF1 API
    
    Args:
        endpoint: API endpoint (e.g., 'meetings', 'sessions')
        params: Query parameters
        
    Returns:
        List of data dictionaries
    """
    def fetch_from_api(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        url = f"{self.api_base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} records from {endpoint}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {endpoint}: {e}")
            return []
            
    # ==================== CACHE CHECKING ====================
    """
    Check if data exists in database
    
    Args:
        table: Table name
        session_key: Optional session filter
        
    Returns:
        True if data exists
    """
    def is_table_cached(self, table: str, session_key: Optional[int] = None) -> bool:
        cursor = self.conn.cursor()
        try:
            if session_key:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE session_key = %s", (session_key,))
            else:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
    
    """Get list of session_keys that have telemetry data cached"""
    def get_cached_sessions(self) -> List[int]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT session_key FROM car_data")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
    
    # ==================== DATA INSERTION ====================
    
    def insert_meetings(self, data: List[Dict]):
        """Insert meetings data"""
        if not data:
            return
        
        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO meetings (
                    meeting_key, circuit_key, circuit_short_name, country_code,
                    country_key, country_name, date_start, gmt_offset,
                    location, meeting_name, meeting_official_name, year
                ) VALUES (
                    %(meeting_key)s, %(circuit_key)s, %(circuit_short_name)s, %(country_code)s,
                    %(country_key)s, %(country_name)s, %(date_start)s, %(gmt_offset)s,
                    %(location)s, %(meeting_name)s, %(meeting_official_name)s, %(year)s
                ) ON CONFLICT (meeting_key) DO NOTHING
            """
            execute_batch(cursor, query, data)
            self.conn.commit()
            logger.info(f"Inserted {len(data)} meetings")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert meetings: {e}")
        finally:
            cursor.close()
    
    def insert_sessions(self, data: List[Dict]):
        """Insert sessions data"""
        if not data:
            return
        
        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO sessions (
                    session_key, meeting_key, circuit_key, circuit_short_name,
                    country_code, country_key, country_name, date_start, date_end,
                    gmt_offset, location, session_name, session_type, year
                ) VALUES (
                    %(session_key)s, %(meeting_key)s, %(circuit_key)s, %(circuit_short_name)s,
                    %(country_code)s, %(country_key)s, %(country_name)s, %(date_start)s, %(date_end)s,
                    %(gmt_offset)s, %(location)s, %(session_name)s, %(session_type)s, %(year)s
                ) ON CONFLICT (session_key) DO NOTHING
            """
            execute_batch(cursor, query, data)
            self.conn.commit()
            logger.info(f"Inserted {len(data)} sessions")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert sessions: {e}")
        finally:
            cursor.close()
    
    def insert_drivers(self, data: List[Dict]):
        """Insert drivers data"""
        if not data:
            return
        
        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO drivers (
                    session_key, meeting_key, driver_number, broadcast_name,
                    country_code, first_name, last_name, full_name,
                    name_acronym, team_name, team_colour, headshot_url
                ) VALUES (
                    %(session_key)s, %(meeting_key)s, %(driver_number)s, %(broadcast_name)s,
                    %(country_code)s, %(first_name)s, %(last_name)s, %(full_name)s,
                    %(name_acronym)s, %(team_name)s, %(team_colour)s, %(headshot_url)s
                ) ON CONFLICT (session_key, driver_number) DO UPDATE SET
                    broadcast_name = EXCLUDED.broadcast_name,
                    team_name = EXCLUDED.team_name,
                    team_colour = EXCLUDED.team_colour
            """
            execute_batch(cursor, query, data)
            self.conn.commit()
            logger.info(f"Inserted {len(data)} driver records")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert drivers: {e}")
        finally:
            cursor.close()
    
    def insert_laps(self, data: List[Dict]):
        """Insert laps data"""
        if not data:
            return
        
        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO laps (
                    session_key, meeting_key, driver_number, lap_number,
                    date_start, lap_duration, is_pit_out_lap,
                    duration_sector_1, duration_sector_2, duration_sector_3,
                    i1_speed, i2_speed, st_speed,
                    segments_sector_1, segments_sector_2, segments_sector_3
                ) VALUES (
                    %(session_key)s, %(meeting_key)s, %(driver_number)s, %(lap_number)s,
                    %(date_start)s, %(lap_duration)s, %(is_pit_out_lap)s,
                    %(duration_sector_1)s, %(duration_sector_2)s, %(duration_sector_3)s,
                    %(i1_speed)s, %(i2_speed)s, %(st_speed)s,
                    %(segments_sector_1)s, %(segments_sector_2)s, %(segments_sector_3)s
                ) ON CONFLICT (session_key, driver_number, lap_number) DO NOTHING
            """
            execute_batch(cursor, query, data)
            self.conn.commit()
            logger.info(f"Inserted {len(data)} laps")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert laps: {e}")
        finally:
            cursor.close()
    
    def insert_car_data(self, data: List[Dict]):
        """Insert car telemetry data (large dataset)"""
        if not data:
            return
        
        cursor = self.conn.cursor()
        try:
            query = """
                INSERT INTO car_data (
                    session_key, meeting_key, driver_number, date,
                    brake, drs, n_gear, rpm, speed, throttle
                ) VALUES (
                    %(session_key)s, %(meeting_key)s, %(driver_number)s, %(date)s,
                    %(brake)s, %(drs)s, %(n_gear)s, %(rpm)s, %(speed)s, %(throttle)s
                )
            """
            # Insert in batches for performance
            batch_size = 5000
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                execute_batch(cursor, query, batch, page_size=1000)
                self.conn.commit()
                logger.info(f"Inserted car_data batch {i//batch_size + 1}/{(len(data)-1)//batch_size + 1}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert car_data: {e}")
        finally:
            cursor.close()
    
    def insert_generic(self, table: str, data: List[Dict]):
        """Generic insert method for simpler tables"""
        if not data:
            return
        
        cursor = self.conn.cursor()
        try:
            # Get column names from first record
            columns = list(data[0].keys())
            placeholders = ', '.join([f"%({col})s" for col in columns])
            cols_str = ', '.join(columns)
            
            query = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
            execute_batch(cursor, query, data)
            self.conn.commit()
            logger.info(f"Inserted {len(data)} records into {table}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert into {table}: {e}")
        finally:
            cursor.close()
    
    # ==================== INITIAL SETUP ====================
    """
    Run initial database population
    
    Args:
        year: Year to start loading from
    """
    def initial_setup(self, year: int = 2025):
        logger.info("Starting initial setup...")
        start_time = time.time()
        
        logger.info("Loading meetings...")
        meetings = self.fetch_from_api('meetings', {'year': year})
        self.insert_meetings(meetings)
        
        logger.info("Loading sessions...")
        sessions = self.fetch_from_api('sessions', {'year': year})
        self.insert_sessions(sessions)
        
        recent_sessions = self.get_recent_sessions(self.config.recent_sessions_count)
        
        for table in self.config.priority_tables:
            if table in ['meetings', 'sessions']:
                continue
            
            logger.info(f"Loading {table}...")
            data = self.fetch_from_api(table, {'year': year})
            
            if table == 'drivers':
                self.insert_drivers(data)
            elif table == 'laps':
                self.insert_laps(data)
            else:
                self.insert_generic(table, data)
            
            time.sleep(0.5)
        
        logger.info(f"Pre-loading telemetry for {len(recent_sessions)} recent sessions...")
        for session_key in recent_sessions:
            self.load_session_telemetry(session_key)
        
        elapsed = time.time() - start_time
        logger.info(f"Initial setup completed in {elapsed:.2f} seconds")
    
    def get_recent_sessions(self, count: int) -> List[int]:
        """Get the N most recent session keys"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT session_key 
                FROM sessions 
                WHERE session_type = 'Race'
                ORDER BY date_start DESC 
                LIMIT %s
            """, (count,))
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
    
    def load_session_telemetry(self, session_key: int):
        """Load all telemetry data for a specific session"""
        logger.info(f"Loading telemetry for session {session_key}...")
        
        # Load car_data
        car_data = self.fetch_from_api('car_data', {'session_key': session_key})
        if car_data:
            self.insert_car_data(car_data)
        
        # Load location
        location_data = self.fetch_from_api('location', {'session_key': session_key})
        if location_data:
            self.insert_generic('location', location_data)
        
        # Load intervals
        intervals_data = self.fetch_from_api('intervals', {'session_key': session_key})
        if intervals_data:
            for record in intervals_data:
                if record.get('gap_to_leader') is not None:
                    record['gap_to_leader'] = str(record['gap_to_leader'])
                if record.get('interval') is not None:
                    record['interval'] = str(record['interval'])
            self.insert_generic('intervals', intervals_data)
        
        # Load position
        position_data = self.fetch_from_api('position', {'session_key': session_key})
        if position_data:
            self.insert_generic('position', position_data)
        
        logger.info(f"Telemetry loaded for session {session_key}")
        
    # loading driver info
    def load_driver_info_by_year(self, year: int = 2025):
        cursor = self.conn.cursor()
        try:
            sessions = self.fetch_from_api('sessions', {'year': year})
            for session in sessions:
                session_key = session['session_key']

                data = self.fetch_from_api('drivers', {'session_key': session_key})                
                self.insert_drivers(data)
        finally:
            cursor.close()

    def load_session_result(self):
        cursor = self.conn.cursor()
        try:
            sessions = self.fetch_from_api('sessions')
            
            for session in sessions:
                session_key = session['session_key']

                datas = self.fetch_from_api('session_result', {'session_key': session_key})  
                for data in datas:
                    data['gap_to_leader'] = str(data['gap_to_leader'])
                    if type(data['duration']) == float:
                        data['duration'] = [data['duration']]
                              
                self.insert_generic('session_result', datas)
        finally:
            cursor.close()
            
    
    # ==================== SMART DATA RETRIEVAL ====================
    """
    Smart data retrieval with automatic caching
    
    Args:
        table: Table name
        session_key: Session key
        filters: Additional WHERE conditions
        
    Returns:
        List of data records
    """
    def get_data(self, table: str, session_key: int, filters: Optional[Dict] = None) -> List[Dict]:
        # Check if data is cached
        if not self.is_table_cached(table, session_key):
            logger.info(f"Cache miss for {table}, session {session_key}. Fetching from API...")
            
            # Fetch from API
            params = {'session_key': session_key}
            if filters:
                params.update(filters)
            
            data = self.fetch_from_api(table, params)
            
            # Store in database
            if table == 'car_data':
                self.insert_car_data(data)
            elif table == 'drivers':
                self.insert_drivers(data)
            elif table == 'laps':
                self.insert_laps(data)
            else:
                self.insert_generic(table, data)
        
        return self.query_table(table, session_key, filters)
    
    def query_table(self, table: str, session_key: int, filters: Optional[Dict] = None) -> List[Dict]:
        """Query data from database"""
        cursor = self.conn.cursor()
        try:
            query = f"SELECT * FROM {table} WHERE session_key = %s"
            params = [session_key]
            
            if filters:
                for key, value in filters.items():
                    query += f" AND {key} = %s"
                    params.append(value)
            
            query += " ORDER BY id LIMIT 1000"
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            logger.info(f"Retrieved {len(results)} records from {table}")
            return results
        finally:
            cursor.close()
            
# if __name__ == "__main__":
#     db_config = {
#         'host': 'localhost',
#         'database': 'f1',
#         'user': 'nawanshaju',
#         'port': 5432
#     }
    
#     with F1DataManager(db_config) as manager:
#         # manager.initial_setup(year=2023)
#         # manager.load_driver_info_by_year(2022)
#         manager.load_session_result()
        
#         # # Example: Get lap data (will use cache if available)
#         # laps = manager.get_data('laps', session_key=9161, filters={'driver_number': 1})
#         # print(f"Retrieved {len(laps)} laps for driver 1")
        
#         # # Example: Get telemetry (will fetch from API if not cached)
#         # telemetry = manager.get_data('car_data', session_key=9161, filters={'driver_number': 1})
#         # print(f"Retrieved {len(telemetry)} telemetry points")
        
#         # Run background backfill (optional, for maintenance)
#         # manager.backfill_popular_sessions(limit=5)