import mysql.connector
from ..config import Config

def get_db_connection():
	db_config = Config.DATABASE_CONFIG
	connection = mysql.connector.connect(**db_config)
	return connection