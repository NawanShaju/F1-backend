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

CREATE TABLE session_result (
    id SERIAL PRIMARY KEY,
    session_key INTEGER NOT NULL REFERENCES sessions(session_key),
    meeting_key INTEGER NOT NULL REFERENCES meetings(meeting_key),
    driver_number INTEGER NOT NULL,
    position INTEGER,
    points INTEGER,
    dnf BOOLEAN DEFAULT FALSE,
    dns BOOLEAN DEFAULT FALSE,
    dsq BOOLEAN DEFAULT FALSE,
    duration NUMERIC(10, 3)[],
    gap_to_leader TEXT,
    number_of_laps INTEGER,
    UNIQUE(session_key, driver_number)
);

