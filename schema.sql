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
    user_id INTEGER REFERENCES users(id),
    image_path TEXT
);

CREATE TABLE picture_classes (
    id INTEGER PRIMARY KEY,
    picture_id INTEGER REFERENCES pictures(id),
    title TEXT,
    style TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    picture_id INTEGER REFERENCES pictures(id),
    user_id INTEGER REFERENCES users(id),
    message TEXT
)