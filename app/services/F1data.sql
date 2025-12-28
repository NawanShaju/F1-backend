CREATE TABLE meetings (
    meeting_key INTEGER PRIMARY KEY,
    circuit_key INTEGER NOT NULL,
    circuit_short_name VARCHAR(100),
    country_code VARCHAR(3),
    country_key INTEGER,
    country_name VARCHAR(100),
    date_start TIMESTAMPTZ NOT NULL,
    gmt_offset INTERVAL,
    location VARCHAR(150),
    meeting_name VARCHAR(200),
    meeting_official_name VARCHAR(300),
    year INTEGER NOT NULL
);

CREATE TABLE sessions (
    session_key INTEGER PRIMARY KEY,
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    circuit_key INTEGER,
    circuit_short_name VARCHAR(100),
    country_code VARCHAR(3),
    country_key INTEGER,
    country_name VARCHAR(100),
    date_start TIMESTAMPTZ NOT NULL,
    date_end TIMESTAMPTZ NOT NULL,
    gmt_offset INTERVAL,
    location VARCHAR(150),
    session_name VARCHAR(50),
    session_type VARCHAR(50),
    year INTEGER NOT NULL
);

CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    broadcast_name VARCHAR(100),
    country_code VARCHAR(3),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200),
    name_acronym VARCHAR(3),
    team_name VARCHAR(100),
    team_colour VARCHAR(6),
    headshot_url TEXT,
    UNIQUE(session_key, driver_number)
);

CREATE TABLE car_data (
    id BIGSERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    brake INTEGER,
    drs INTEGER,
    n_gear INTEGER,
    rpm INTEGER,
    speed INTEGER,
    throttle INTEGER
);

CREATE INDEX idx_car_data_session_driver ON car_data(session_key, driver_number);
CREATE INDEX idx_car_data_date ON car_data(date);

CREATE TABLE location (
    id BIGSERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    x INTEGER,
    y INTEGER,
    z INTEGER
);

CREATE INDEX idx_location_session_driver ON location(session_key, driver_number);
CREATE INDEX idx_location_date ON location(date);

CREATE TABLE laps (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    lap_number INTEGER NOT NULL,
    date_start TIMESTAMPTZ,
    lap_duration NUMERIC(10, 3),
    is_pit_out_lap BOOLEAN,
    duration_sector_1 NUMERIC(10, 3),
    duration_sector_2 NUMERIC(10, 3),
    duration_sector_3 NUMERIC(10, 3),
    i1_speed INTEGER,
    i2_speed INTEGER,
    st_speed INTEGER,
    segments_sector_1 INTEGER[],
    segments_sector_2 INTEGER[],
    segments_sector_3 INTEGER[],
    UNIQUE(session_key, driver_number, lap_number)
);

CREATE INDEX idx_laps_session ON laps(session_key);
CREATE INDEX idx_laps_driver ON laps(driver_number);

CREATE TABLE pit (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    lap_number INTEGER,
    pit_duration NUMERIC(10, 3)
);

CREATE INDEX idx_pit_session ON pit(session_key);

CREATE TABLE stints (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    stint_number INTEGER NOT NULL,
    lap_start INTEGER,
    lap_end INTEGER,
    compound VARCHAR(20),
    tyre_age_at_start INTEGER,
    UNIQUE(session_key, driver_number, stint_number)
);

CREATE TABLE position (
    id BIGSERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    position INTEGER NOT NULL
);

CREATE INDEX idx_position_session_driver ON position(session_key, driver_number);
CREATE INDEX idx_position_date ON position(date);

CREATE TABLE intervals (
    id BIGSERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    gap_to_leader NUMERIC(10, 3),
    interval NUMERIC(10, 3)
);

CREATE INDEX idx_intervals_session ON intervals(session_key);
CREATE INDEX idx_intervals_date ON intervals(date);

CREATE TABLE race_control (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    date TIMESTAMPTZ NOT NULL,
    category VARCHAR(50),
    flag VARCHAR(50),
    scope VARCHAR(50),
    sector INTEGER,
    driver_number INTEGER,
    lap_number INTEGER,
    message TEXT
);

CREATE INDEX idx_race_control_session ON race_control(session_key);
CREATE INDEX idx_race_control_date ON race_control(date);

CREATE TABLE team_radio (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    recording_url TEXT
);

CREATE INDEX idx_team_radio_session_driver ON team_radio(session_key, driver_number);

CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    date TIMESTAMPTZ NOT NULL,
    air_temperature NUMERIC(5, 2),
    humidity INTEGER,
    pressure NUMERIC(6, 2),
    rainfall BOOLEAN,
    track_temperature NUMERIC(5, 2),
    wind_direction INTEGER,
    wind_speed NUMERIC(5, 2)
);

CREATE INDEX idx_weather_session ON weather(session_key);

CREATE TABLE overtakes (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    date TIMESTAMPTZ NOT NULL,
    overtaking_driver_number INTEGER NOT NULL,
    overtaken_driver_number INTEGER NOT NULL,
    position INTEGER
);

CREATE INDEX idx_overtakes_session ON overtakes(session_key);

CREATE TABLE session_result (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    position INTEGER,
    dnf BOOLEAN DEFAULT FALSE,
    dns BOOLEAN DEFAULT FALSE,
    dsq BOOLEAN DEFAULT FALSE,
    duration NUMERIC(10, 3)[],
    gap_to_leader TEXT[],
    number_of_laps INTEGER,
    UNIQUE(session_key, driver_number)
);

CREATE TABLE starting_grid (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    position INTEGER NOT NULL,
    lap_duration NUMERIC(10, 3),
    UNIQUE(session_key, driver_number)
);

