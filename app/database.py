import os
from dotenv import load_dotenv
load_dotenv()

import mysql.connector 

mydb = mysql.connector.connect(
    host = os.environ.get("DB_HOST"),
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    database = os.environ.get("DB_DATABASE")
)
