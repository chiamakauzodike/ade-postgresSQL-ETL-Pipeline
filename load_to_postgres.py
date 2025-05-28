import pandas as pd
import psycopg2
import csv
from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT, URL

# Loading to Database Layer
# develop a function to connect to pgadmin
def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return connection
   
conn = get_db_connection()

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create schema
    cursor.execute("CREATE SCHEMA IF NOT EXISTS unidata;")

    # Drop tables (in reverse FK order)
    cursor.execute("DROP TABLE IF EXISTS unidata.fact_university_ranking;")
    cursor.execute("DROP TABLE IF EXISTS unidata.dim_location;")
    cursor.execute("DROP TABLE IF EXISTS unidata.dim_institution;")

    # Create dim_location
    cursor.execute('''
        CREATE TABLE unidata.dim_location (
            city TEXT,
            country TEXT,
            continent TEXT,
            location_id SERIAL PRIMARY KEY
        );
    ''')

    # Create dim_institution
    cursor.execute('''
        CREATE TABLE unidata.dim_institution (     
            name TEXT NOT NULL,
            affiliation TEXT,
            attend_mode TEXT,
            founded INT,
            link TEXT,
            institution_id SERIAL PRIMARY KEY
        );
    ''')

    # Create fact table
    cursor.execute('''
        CREATE TABLE unidata.fact_university_ranking (
            fact_id SERIAL PRIMARY KEY,
            rank INT,
            institution_id INT REFERENCES unidata.dim_institution(institution_id),
            location_id INT REFERENCES unidata.dim_location(location_id),   
            enrollment INT
        );
    ''')

    conn.commit()
    cursor.close()
    conn.close()

create_tables()

def load_data_from_csv_to_table(csv_path, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        
        for row in reader:
            placeholders = ', '.join(['%s'] * len(row))
            query = f'INSERT INTO {table_name} VALUES ({placeholders});'
            cursor.execute(query, row)  # <-- Missing line added here

    conn.commit()
    cursor.close()
    conn.close()

fact_csv_path = 'dim_institution.csv'
load_data_from_csv_to_table(fact_csv_path, 'unidata.dim_institution')

fact_csv_path = 'dim_location.csv'
load_data_from_csv_to_table(fact_csv_path, 'unidata.dim_location')

# fact table
fact_csv_path = 'fact_university_ranking.csv'
load_data_from_csv_to_table(fact_csv_path, 'unidata.fact_university_ranking')

print("All Data has been loaded successfully into their respective schema and tables")