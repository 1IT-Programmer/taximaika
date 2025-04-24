import sqlite3

def create_connection():
    connection = sqlite3.connect("transport.db")
    return connection
