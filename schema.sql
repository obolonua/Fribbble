CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE pictures (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    style TEXT,
    user_id INTEGER REFERENCES users,
    image_path TEXT
);