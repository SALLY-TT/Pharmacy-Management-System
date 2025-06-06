
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0411",
        database="yaofang2"
    )
    return conn
