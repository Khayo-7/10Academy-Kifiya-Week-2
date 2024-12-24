import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def execute_queries(query):
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return pd.read_sql_query(query, engine)

def get_unique_imsi_count():
    query = """
                SELECT COUNT(DISTINCT "IMSI") AS "Unique IMSI Count"
                FROM xdr_data;
            """
    return execute_queries(query)

def get_average_duration():
    query = """
                SELECT AVG("Dur. (ms)") AS "Average Duration"
                FROM xdr_data
                WHERE "Dur. (ms)" IS NOT NULL;
            """
    return execute_queries(query)

def get_total_data_usage():
    query = """
                SELECT "IMSI", 
                    SUM("Total UL (Bytes)") AS "Total UL Bytes", 
                    SUM("Total DL (Bytes)") AS "Total DL Bytes"
                FROM xdr_data
                GROUP BY "IMSI"
                ORDER BY "Total DL Bytes" DESC
                LIMIT 10;
            """
    return execute_queries(query)

def get_top_10_handsets():
    query = """
                SELECT 
                    "Handset Type" AS "Handset",
                    COUNT(*) AS "Usage Count"
                FROM xdr_data
                GROUP BY "Handset Type"
                ORDER BY "Usage Count" DESC
                LIMIT 10;
            """
    return execute_queries(query)

def get_top_3_manufacturers():
    query = """
                SELECT 
                    "Handset Manufacturer",
                    COUNT(*) AS "Usage Count"
                FROM xdr_data
                GROUP BY "Handset Manufacturer"
                ORDER BY "Usage Count" DESC
                LIMIT 3;
            """
    return execute_queries(query)

def get_top_handsets_by_manufacturers():
    query = """
                WITH TopManufacturers AS (
                    SELECT 
                        "Handset Manufacturer"
                    FROM xdr_data
                    GROUP BY "Handset Manufacturer"
                    ORDER BY COUNT(*) DESC
                    LIMIT 3
                )
                SELECT 
                    "Handset Manufacturer",
                    "Handset Type",
                    COUNT(*) AS "Usage Count"
                FROM xdr_data
                WHERE "Handset Manufacturer" IN (SELECT "Handset Manufacturer" FROM TopManufacturers)
                GROUP BY "Handset Manufacturer", "Handset Type"
                ORDER BY "Handset Manufacturer", "Usage Count" DESC;
            """
    return execute_queries(query)

def get_total_data_usage_by_user():
    query = """
                SELECT 
                    "MSISDN/Number" AS "MSISDN",
                    COUNT(*) AS "Session Frequency",
                    SUM("Dur. (ms)") AS "Total Session Duration",
                    SUM("Total UL (Bytes)") AS "Total UL (Bytes)",
                    SUM("Total DL (Bytes)") AS "Total DL (Bytes)",
                    SUM("Total UL (Bytes)" + "Total DL (Bytes)") AS "Total Data (Bytes)"
                FROM xdr_data
                GROUP BY "MSISDN/Number"
                ORDER BY "Total Data (Bytes)" DESC;
            """
    return execute_queries(query)

def get_avg_duration_by_location():
    query = """
                SELECT 
                    "Last Location Name",
                    AVG("Dur. (ms)") AS "Avg Duration"
                FROM xdr_data
                GROUP BY "Last Location Name"
                ORDER BY "Avg Duration" DESC;
            """
    return execute_queries(query)

def get_avg_duration_by_manufacturer():
    query = """
                SELECT 
                    "Handset Manufacturer",
                    AVG("Dur. (ms)") AS "Avg Duration"
                FROM xdr_data
                GROUP BY "Handset Manufacturer"
                ORDER BY "Avg Duration" DESC;
            """
    return execute_queries(query)

def get_avg_duration_by_handset_type():
    query = """
                SELECT 
                    "Handset Type",
                    AVG("Dur. (ms)") AS "Avg Duration"
                FROM xdr_data
                GROUP BY "Handset Type"
                ORDER BY "Avg Duration" DESC;
            """
    return execute_queries(query)

def get_total_data_usage_by_application(application):
    query = f"""
                SELECT 
                    "MSISDN/Number" AS "UserID",
                    "Total DL (Bytes)" + "Total UL (Bytes)" AS "Total Data (Bytes)",
                    "{application} UL (Bytes)" + "{application} DL (Bytes)" AS "Application Data Volume"
                FROM xdr_data
                ORDER BY "Total Data (Bytes)" DESC;
            """
    return execute_queries(query)
