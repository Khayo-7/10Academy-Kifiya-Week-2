import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def load_data_from_postgres_db(query):

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def load_data_using_sqlalchemy(query):
    
    try:
        # connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)   
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def load_data_to_db(file_path, table_name):
    
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Data from {file_path} loaded to {table_name} table successfully.")
