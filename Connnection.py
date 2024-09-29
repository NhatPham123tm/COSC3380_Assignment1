import psycopg2
from psycopg2 import OperationalError
import os

def connect_to_db():
    # Define our connection parameters
    db_params = {
        "host": "127.0.0.1",
        "dbname": "cosc3380",
        "user": "dbs34",
        "port": "5432",
        "password": "Team343380"
    }

    try:
        # Attempt to establish a connection
        print("Connecting to database...")
        conn = psycopg2.connect(**db_params)
        
        # Create a cursor
        cursor = conn.cursor()
        
        print("Connected successfully!")
        return conn, cursor
    
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None, None
    
def close(cursor, connection):
    cursor.close()
    connection.close()
    print("Database connection closed.")

def check_file_exists(file_path):
    # Method 1: Using os.path.exists()
    if os.path.exists(file_path):
        print(f"File exists : {file_path}")
    else:
        print(f"File does not exist : {file_path}")

def set_search_path(cursor, sql_query=""):
    print(f"Query : {sql_query}")
    cursor.execute(sql_query)
    # Verify the search_path
    cursor.execute("SHOW search_path;")
    records = cursor.fetchall()
    for record in records :
        print ( record )
        
def get_filename_without_extension(filepath):
    # Get the base name (filename with extension, without path)
    base_name = os.path.basename(filepath)
    # Split the base name and return just the filename without extension
    return os.path.splitext(base_name)[0]