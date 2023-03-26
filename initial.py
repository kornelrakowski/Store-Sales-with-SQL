import mysql.connector
from mysql.connector import errorcode

config = {
	'user': 'root', 
	'password': 'Supreme',
	'host': '127.0.0.1',
	'allow_local_infile': True,
	'get_warnings': True
}

DB_NAME = 'store_sales'

datasets = ['train', 'transactions', 'stores', 'oil', 'holidays_events', 'test']

def initial():

	TABLES = {}

	TABLES['train'] = """CREATE TABLE IF NOT EXISTS train (
		id INT,
		date DATE,
		store_nbr INT,
		family VARCHAR(100),
		sales DECIMAL(16,2),
		onpromotion INT,
		PRIMARY KEY (id)
		)"""
	
	TABLES['transactions'] = """CREATE TABLE IF NOT EXISTS transactions (
		date DATE,
		store_nbr INT,
		transactions INT
		)"""

	TABLES['stores'] = """CREATE TABLE IF NOT EXISTS stores (
		store_nbr INT,
		city VARCHAR(100),
		state VARCHAR(100),
		type VARCHAR(2),
		cluster INT,
		PRIMARY KEY (store_nbr)
		)"""

	TABLES['oil'] = """CREATE TABLE IF NOT EXISTS oil (
		date DATE,
		oil_price DECIMAL(5,2),
		PRIMARY KEY (date)
		)"""
	
	TABLES['holidays_events'] = """CREATE TABLE IF NOT EXISTS holidays_events (
		date DATE,
		type VARCHAR(100),
		locale VARCHAR(100),
		locale_name VARCHAR(100),
		description VARCHAR(100),
		transferred VARCHAR(10),
		PRIMARY KEY (date)
		)"""
	
	TABLES['test'] = """CREATE TABLE IF NOT EXISTS test (
		id INT,
		date DATE,
		store_nbr INT,
		family VARCHAR(100),
		sales DECIMAL(16,2),
		onpromotion INT,
		PRIMARY KEY (id)
		)"""

	database = mysql.connector.connect(**config)
	cursor = database.cursor()

	#	CREATE DATABASE
	cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(DB_NAME))
	cursor.execute('USE {}'.format(DB_NAME))

	#	CREATE TABLES
	for table_name in TABLES:
		table_description = TABLES[table_name]
		cursor.execute(table_description)

	#	DOWNLOAD SOURCE CSV FILES

	#	LOAD DATA TO TABLES FROM CSV FILES
	for dataset_name in datasets:
		import_csv = """LOAD DATA LOCAL INFILE '/home/kormel/Desktop/Store Sales with SQL/datasets/{dataset_name}.csv'
		INTO TABLE {dataset_name}
		FIELDS TERMINATED BY ','
		ENCLOSED BY '"'
		LINES TERMINATED BY '\n'
		IGNORE 1 ROWS
		""".format(dataset_name=dataset_name)
		cursor.execute(import_csv)
		database.commit()

	cursor.close()
	database.close()

initial()