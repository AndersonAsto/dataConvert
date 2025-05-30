import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{os.getenv('SQL_DRIVER')}}};"
            f"SERVER={os.getenv('SQL_SERVER')};"
            f"DATABASE={os.getenv('SQL_DATABASE')};"
            f"UID={os.getenv('SQL_USERNAME')};"
            f"PWD={os.getenv('SQL_PASSWORD')};"
        )
        return conn
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None