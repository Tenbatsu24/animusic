from database import Connection

create_schema = "CREATE SCHEMA music_data; SET search_path = music_data, public;"
create_tables = """
    CREATE TABLE anime (
        id int PRIMARY KEY,
        name varchar
    );
    
    CREATE TABLE artist (
        id SERIAL PRIMARY KEY,
        name varchar
    );

    CREATE TABLE song (
        id SERIAL PRIMARY KEY,
        name varchar,
        artistID int,
        fullURL varchar,
        abridgedURL varchar,
        FOREIGN KEY (artistID) REFERENCES artist(id) ON DELETE CASCADE
    );

    CREATE TABLE song_anime (
        songID int,
        animeID int,
        episodes varchar,
        PRIMARY KEY (songID, animeID),
        FOREIGN KEY (songID) REFERENCES song(id) ON DELETE CASCADE,
        FOREIGN KEY (animeID) REFERENCES anime(id) ON DELETE CASCADE
    );

    CREATE TABLE opening (
        id int PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES song(id) ON DELETE CASCADE
    );

    CREATE TABLE ending (
        id int PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES song(id) ON DELETE CASCADE
    );
"""

conn = Connection()

conn.acquire('animusic')
conn.execute(create_schema)
conn.execute(create_tables)
conn.commit()
