from typing import List
from psycopg2.extras import execute_values

CREATE_PLAYLIST = """CREATE TABLE IF NOT EXISTS playlists
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_SONG = """CREATE TABLE IF NOT EXISTS songs
(id SERIAL PRIMARY KEY, song_title TEXT, playlist_id INTEGER, FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE);"""
CREATE_USER = """CREATE TABLE IF NOT EXISTS users
(username TEXT, playlist_id INTEGER, FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE);"""

INSERT_PLAYLIST_RETURN_ID = "INSERT INTO playlists (title, owner_username) VALUES (%s, %s) RETURNING id;"
INSERT_SONG = "INSERT INTO songs (song_title, playlist_id) VALUES %s;"
INSERT_SONG_PLAYLIST = "INSERT INTO songs (song_title, playlist_id) VALUES (%s, %s);"

SELECT_ALL_PLAYLIST = "SELECT * FROM playlists;"
SELECT_PLAYLIST_WITH_SONGS = """SELECT * FROM songs
JOIN playlists ON songs.playlist_id = playlists.id
WHERE playlists.id = %s"""
SELECT_PLAYLIST = """SELECT * FROM playlists
JOIN songs ON songs.playlist_id = playlists.id
WHERE playlists.id = %s"""
SELECT_RANDOM_SONG_FROM_PLAYLIST = """SELECT * FROM songs
WHERE playlist_id = %s ORDER BY RANDOM() DESC LIMIT 1;"""
SELECT_SONG = """SELECT playlists.id, playlists.title FROM SONGS
JOIN playlists ON playlists.id = songs.playlist_id
WHERE songs.song_title = %s"""

DELETE_PLAYLIST = "DELETE FROM playlists WHERE title = %s;"


def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PLAYLIST)
            cursor.execute(CREATE_SONG)
            cursor.execute(CREATE_USER)


def create_playlist(connection, playlist_title: str, playlist_owner: str, songs: List[str]):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_PLAYLIST_RETURN_ID, (playlist_title, playlist_owner))

            playlist_id = cursor.fetchone()[0]
            song_values = [(song_title, playlist_id) for song_title in songs]

            execute_values(cursor, INSERT_SONG, song_values)


def add_song_to_playlist(connection, playlist, song_title):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_SONG_PLAYLIST, (song_title, playlist))


def get_playlist(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_PLAYLIST)
            return cursor.fetchall()

def get_playlist_with_songs(connection, playlist_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_PLAYLIST_WITH_SONGS, (playlist_id,))
            return cursor.fetchall()


def delete_playlist(connection, playlist_title):
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(DELETE_PLAYLIST, (playlist_title,))
            except ValueError:
                print("Oops! Playlist not found :(")


def select_random_song(connection, playlist_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_SONG_FROM_PLAYLIST, (playlist_id,))
            return cursor.fetchall()


def search_song(connection, song_title):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_SONG, (song_title,))
            return cursor.fetchall()