import random
from time import sleep

import psycopg2

from database import Connection
from scraper import scrape

add_anime = lambda idx, anime: f"""INSERT INTO anime (id, name) VALUES ({idx}, '{anime}');"""
add_artist = lambda artist: f"""INSERT INTO artist (id, name) VALUES (DEFAULT, '{artist}') RETURNING id;"""
add_song = lambda song, artist_idx: \
    f"""INSERT INTO song (id, name, artistID) VALUES (DEFAULT, '{song}', {artist_idx}) RETURNING id;"""
add_song_anime = lambda song_idx, anime_idx, ep: f"""INSERT INTO song_anime VALUES ({song_idx}, {anime_idx}, '{ep}');"""
add_oped = lambda op, song_idx: f"""INSERT INTO {'opening' if op else 'ending'} VALUES ({song_idx});"""

try:
    connection = Connection()
    artists = dict()
    count = 0

    for i in range(37232, 50000):
        sleep(10*random.random())
        first = True
        connection.acquire('music_data')
        for (anime_id, anime_name, ops) in scrape(i):
            # print(f"adding anime {i} to db")
            if first:
                connection.execute(add_anime(anime_id, anime_name))
            for (song_name, artist_name, eps) in ops:
                # print("OP" if first else "ED", song_name, artist, eps)
                if artist_name not in artists.keys():
                    connection.execute(add_artist(artist_name))
                    artists[artist_name] = connection.fetch()[0][0]

                artist_id = artists[artist_name]
                connection.execute(add_song(song_name, artist_id))

                song_id = connection.fetch()[0][0]
                connection.execute(add_song_anime(song_id, anime_id, eps))

                connection.execute(add_oped(first, song_id))
            first = False
        connection.commit()

except psycopg2.Error as error:
    print(error)
finally:
    connection.close()
