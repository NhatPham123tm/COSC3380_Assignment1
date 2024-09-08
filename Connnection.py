import psycopg2
from psycopg2 import OperationalError

def connect_to_db():
    # Define our connection parameters
    db_params = {
        "host": "localhost",
        "dbname": "Ruuby_data",
        "user": "postgres",
        "port": "5432",
        "password": "Ruby0909"  # It's better to use environment variables for passwords
    }

    # Alternative connection string for different setup (commented out)
    # db_params = {
    #     "dbname": "COSC3380",
    #     "user": "cosc0218",
    #     "password": "1642106AS",
    #     "host": "code.cs.uh.edu",
    #     "port": "5432",
    #     "sslmode": "require"
    # }

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
    
def main():
    # Usage
    connection, cursor = connect_to_db()

    if connection:
        # Your database operations here
        
        # Don't forget to close the connection when you're done
        cursor.close()
        connection.close()
        print("Database connection closed.")
 
if __name__ == "__main__":
    main()