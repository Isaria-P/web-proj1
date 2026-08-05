CREATE TABLE IF NOT EXISTS Cams (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    img VARCHAR(255),
    category TEXT NOT NULL,
    author TEXT NOT NULL,
    created DATETIME NOT NULL
);