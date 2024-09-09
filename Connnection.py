import psycopg2
from psycopg2 import OperationalError

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
 