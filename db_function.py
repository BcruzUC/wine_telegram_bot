from dotenv import load_dotenv
import os


load_dotenv(encoding='UTF-8')

dbname = os.getenv('DBNAME')
dbuser = os.getenv('DBUSER')
dbpass = os.getenv('DBPASS')
dbhost = os.getenv('DBHOST')

connection_string = f"dbname={dbname} user={dbuser} password={dbpass} host={dbhost}"