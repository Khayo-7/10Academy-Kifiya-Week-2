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
                SELECT COUNT(DISTINCT "IMSI") AS unique_imsi_count
                FROM xdr_data;
            """
    return execute_queries(query)

def get_average_duration():
    query = """
                SELECT AVG("Dur. (ms)") AS average_duration
                FROM xdr_data
                WHERE "Dur. (ms)" IS NOT NULL;
            """
    return execute_queries(query)

def get_total_data_usage():
    query = """
                SELECT "IMSI", 
                    SUM("Total UL (Bytes)") AS total_ul_bytes, 
                    SUM("Total DL (Bytes)") AS total_dl_bytes
                FROM xdr_data
                GROUP BY "IMSI"
                ORDER BY total_dl_bytes DESC
                LIMIT 10;
            """
    return execute_queries(query)

def get_top_10_handsets():
    query = """
                SELECT 
                    "Handset Type" AS Handset,
                    COUNT(*) AS UsageCount
                FROM xdr_data
                GROUP BY "Handset Type"
                ORDER BY UsageCount DESC
                LIMIT 10;
            """
    return execute_queries(query)

def get_top_3_manufacturers():
    query = """
                SELECT 
                    "Handset Manufacturer",
                    COUNT(*) AS UsageCount
                FROM xdr_data
                GROUP BY "Handset Manufacturer"
                ORDER BY UsageCount DESC
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
                    COUNT(*) AS UsageCount
                FROM xdr_data
                WHERE "Handset Manufacturer" IN (SELECT "Handset Manufacturer" FROM TopManufacturers)
                GROUP BY "Handset Manufacturer", "Handset Type"
                ORDER BY "Handset Manufacturer", UsageCount DESC;
            """
    return execute_queries(query)

def get_total_data_usage_by_user():
    query = """
                SELECT 
                    "MSISDN" AS UserID,
                    COUNT(*) AS NumberOfSessions,
                    SUM("Dur. (ms)") AS TotalSessionDuration,
                    SUM("Total UL (Bytes)") AS TotalUploadData,
                    SUM("Total DL (Bytes)") AS TotalDownloadData,
                    SUM("Total UL (Bytes)" + "Total DL (Bytes)") AS TotalDataVolume
                FROM xdr_data
                GROUP BY "MSISDN"
                ORDER BY TotalDataVolume DESC;
            """
    return execute_queries(query)

def get_avg_duration_by_location():
    query = """
                SELECT 
                    "Last Location Name",
                    AVG("Dur. (ms)") AS AvgDuration
                FROM xdr_data
                GROUP BY "Last Location Name"
                ORDER BY AvgDuration DESC;
            """
    return execute_queries(query)

def get_avg_duration_by_manufacturer():
    query = """
                SELECT 
                    "Handset Manufacturer",
                    AVG("Dur. (ms)") AS AvgDuration
                FROM xdr_data
                GROUP BY "Handset Manufacturer"
                ORDER BY AvgDuration DESC;
            """
    return execute_queries(query)

def get_avg_duration_by_handset_type():
    query = """
                SELECT 
                    "Handset Type",
                    AVG("Dur. (ms)") AS AvgDuration
                FROM xdr_data
                GROUP BY "Handset Type"
                ORDER BY AvgDuration DESC;
            """
    return execute_queries(query)

def get_total_data_usage_by_application(application):
    query = f"""
                SELECT 
                    "MSISDN" AS UserID,
                    "Total DL (Bytes)" + "Total UL (Bytes)" AS TotalDataVolume,
                    "{application} UL (Bytes)" + "{application} DL (Bytes)" AS ApplicationDataVolume
                FROM xdr_data
                ORDER BY TotalDataVolume DESC;
            """
    return execute_queries(query).groupby('ApplicationDataVolume')['TotalDataVolume']
