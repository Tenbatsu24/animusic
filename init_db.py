from database import Connection

create_schema = "CREATE SCHEMA music_data; SET search_path = music_data, public;"
create_tables = """
    CREATE TABLE anime (
        id SERIAL PRIMARY KEY,
        name varchar
    );

    CREATE TABLE song (
        id SERIAL PRIMARY KEY,
        name varchar,
        artist varchar,
        fullURL varchar,
        abridgedURL varchar
    );

    CREATE TABLE song_anime (
        songID int,
        animeID int,
        episodes varchar,
        PRIMARY KEY (songID, animeID),
        FOREIGN KEY (songID) REFERENCES music_data.song(id),
        FOREIGN KEY (animeID) REFERENCES music_data.anime(id)
    );

    CREATE TABLE opening (
        id int PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES music_data.song(id)
    );

    CREATE TABLE ending (
        id int PRIMARY KEY,
        FOREIGN KEY (id) REFERENCES music_data.song(id)
    );
"""

conn = Connection()

conn.acquire()
conn.execute(create_schema)
conn.execute(create_tables)
conn.commit()
