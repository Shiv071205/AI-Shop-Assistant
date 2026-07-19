import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),  
        database="shopassistant"
    )
