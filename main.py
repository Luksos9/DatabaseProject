import os
from typing import List
import psycopg2
from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
import database

DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "

MENU_PROMPT = """-- Menu --

1) create playlist
2) Add new song to playlist
3) Show all playlist
4) Show playlist's songs
5) Delete playlist
6) Select a random song
7) Search Song
8) Exit 

Enter your choice: """

NEW_SONG_PROMPT = "Enter new song (or leave empty to stop adding songs): "


def prompt_create_playlist(connection):
    playlist_title = input("Enter playlist title: ")
    playlist_owner = input("Enter playlist owner: ")
    songs = []

    while (new_song := input(NEW_SONG_PROMPT)):
        songs.append(new_song)

    database.create_playlist(connection, playlist_title, playlist_owner, songs)


def prompt_add_new_song_playlist(connection):
    playlist_id = int(input("Enter playlist id that you would like to add song to: "))
    song_title = input("Enter song's title: ")

    try:
        database.add_song_to_playlist(connection, playlist_id, song_title)
    except ValueError:
        print("Wrong input!")

def prompt_list_all_playlist(connection):
    playlists = database.get_playlist(connection)

    for _id, title, owner in playlists:
        print(f"{_id}: {title} (created by {owner})")
    print()


def prompt_show_playlist_with_songs(connection):
    playlist_title = int(input("Enter playlist's id: "))
    playlists_with_songs = database.get_playlist_with_songs(connection, playlist_title)
    print(f"----- {playlists_with_songs[0][4]} -----")
    for pos, song in enumerate(playlists_with_songs):
        print(f"{pos+1}: {song[1]}")
    print("--"*10)
    print()


def prompt_delete_playlist(connection):
    playlist_title = input("Enter playlist's title that you would like to delete: ")

    database.delete_playlist(connection, playlist_title)


def prompt_select_random_song_from_playlist(connection):
    playlist_id = int(input("Enter playlist's id that you would like to select random song from: "))
    song = database.select_random_song(connection, playlist_id)
    for _id, title, _playlist_id in song:
        print(f"Random song: {title} (playlist id: {_playlist_id})")
    print()

def prompt_search_song(connection):
    song_title = input("Select song that you would like to search: ")
    song = database.search_song(connection, song_title)
    for _playlist_id, _playlist_title in song:
        print("This song is in playlist:")
        print(f"ID: {_playlist_id}, Title: {_playlist_title}\n")

MENU_OPTIONS = {
    "1": prompt_create_playlist,
    "2": prompt_add_new_song_playlist,
    "3": prompt_list_all_playlist,
    "4": prompt_show_playlist_with_songs,
    "5": prompt_delete_playlist,
    "6": prompt_select_random_song_from_playlist,
    "7": prompt_search_song,
}


def menu():
    database_uri = input(DATABASE_PROMPT)
    if not database_uri:
        load_dotenv()
        database_uri = os.environ["DATABASE_URI"]

    connection = psycopg2.connect(database_uri)
    database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "8":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()
