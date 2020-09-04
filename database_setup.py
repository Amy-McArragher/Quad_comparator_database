import psycopg2
import datetime
from comparator import main
import time 
import re

def get_connection():
	con = psycopg2.connect(user="admin", password="admin", host = "127.0.0.1",port = "5432",database="comparator")
	cursor = con.cursor()
	print("database connected")
	return con,cursor


def create_database(con,cursor):
	'''for changing the table if I get it wrong'''
	create_table_results_query = '''CREATE TABLE Results
	(created_at date,
	domain VARCHAR(10000) NOT NULL,
	quad_9 boolean,
	quad9_noblock boolean,
	google boolean,
	cloudflare_safe boolean,
	cloudflare boolean,
	opendns boolean,
	ultrarecursive boolean);'''#need to put date back into this
	create_table_sources_query = '''CREATE TABLE Sources
	(domain VARCHAR(10000) NOT NULL,
	source VARCHAR(20) NOT NULL,
	created_at date NOT NULL);'''
	create_table_domains_query = '''CREATE TABLE Domains
	(domain VARCHAR(10000) PRIMARY KEY,
	number_sources INT NOT NULL,
	registrar VARCHAR(20));'''
	cursor.execute(create_table_results_query)
	con.commit()
	cursor.execute(create_table_sources_query)
	con.commit()
	cursor.execute(create_table_domains_query)
	con.commit()
	print("tables created")


def delete_database(con,cursor):
	'''for changing the table if I get it wrong'''
	try:
		cursor.execute("DROP TABLE Results;")
	except psycopg2.errors.UndefinedTable:
		print("Table Results doesn't exist")
	try:
		cursor.execute("DROP TABLE Sources;")
	except psycopg2.errors.UndefinedTable:
		print("Table Sources doesn't exist")
	try:
		cursor.execute("DROP TABLE Domains;")
	except psycopg2.errors.UndefinedTable:
		print("Table Domains doesn't exist")
	con.commit()
	print("tables deleted")


def URL_filter(URL):
	if " " in URL:
		return []
	URL = URL.split("/")
	#print(URL)
	try:
		for x in range(0,3):
			#print(URL[x])
			URL_return = re.findall(".+\.[a-z]+",URL[x])
			if len(URL_return) != 0:
				#print(URL_return)
				break
	except IndexError:
		
		return URL_return
	return URL_return


def import_sources(con,cursor):
	sources_file = open("source_files.txt","r")
	sources = sources_file.readlines()
	sources_file.close()
	#print(sources)
	source_split = []
	for value in sources:
		value = value.strip()
		source_split.append(value.split(","))
	for value in source_split:
		source_filename = value[0]
		source_name = value[1]
		print("NOW EXTRACTING FROM:", source_name)
		print("\n\n\n\n\n\n\n")
		import_from_source(con,cursor,source_filename,source_name)
		run_comparator(con,cursor,source_name)
	

def import_from_source(con,cursor,source_filename,source_name):
	'''each time a new source is added run this'''
	date = datetime.date.today()
	#source_filename = input("Please enter the name of the source file you want to input\n")
	#source_name = input("Please enter the name of the source\n")
	#source_filename = source_filename + ".txt"
	file = open(source_filename,"r")
	URL_list = file.readlines()
	input_array_domains = []
	input_array_sources = []
	URL_list = list(dict.fromkeys(URL_list))
	filtered_URL_list = []
	for URL in URL_list:
		if URL != "":
			URL = URL.strip()
			URL = URL.lower()
			URL = URL_filter(URL)
			if len(URL) != 0:#append to list here to check for duplicates
				filtered_URL_list.append(URL[0])
	filtered_URL_list = list(dict.fromkeys(filtered_URL_list))
	#print(filtered_URL_list)
	for URL in filtered_URL_list:
		original = True
		input_list = []
		input_list.append(URL)
		input_list.append(source_name)
		input_list.append(str(date))
		SQL_command = "INSERT INTO Sources (domain, source, created_at) VALUES (%s , %s, %s)"
		cursor.execute(SQL_command, input_list)
		SQL_CHECK = "SELECT domain FROM Domains WHERE domain = %s"
		#tuple_url = tuple(URL)
		cursor.execute(SQL_CHECK,(URL,))
		con.commit()
		repeat = cursor.fetchall()
		if len(repeat) != 0:
			#print("update needed",URL)
			original = False
			for value in repeat:
				SQL_update = "UPDATE domains SET number_sources = number_sources + 1 WHERE domain = %s;"
				cursor.execute(SQL_update,(URL,))
				con.commit()
		if original:
			to_input = []
			to_input.append(URL)
			to_input.append(1)
			input_array_domains.append(to_input)
		#input_array_sources.append(input_list)
	update_domain(con,cursor,input_array_domains)
	con.commit()
	

def update_domain(con,cursor,URL_list):
	'''also run each time a new source is added'''
	print("inserting into domains")
	SQL_query = '''INSERT INTO Domains (domain,number_sources) VALUES (%s, %s)'''
	cursor.executemany(SQL_query,URL_list)
	con.commit()
	print("sources uploaded")
		
	
def run_comparator(con,cursor,source_name):
	'''Lees code is called from here'''
	main(con,cursor,source_name)


def main_run():
	start_again = input("Would you like to delete the current database and start a new one?(Y/N)")
	start_time =time.time()
	con,cursor = get_connection()
	if start_again == "Y":
		delete_database(con,cursor)
		create_database(con,cursor)
	import_sources(con,cursor)
	print("--- %s seconds ---" % (time.time() - start_time))
	time_value = time.time() - start_time
	return time_value


#code for texting how long it would take to run through the project.
times = []
repeat = 1
for x in range(repeat):
	time_value = main_run()
	times.append(time_value)
time_total = 0
for value in times:
	time_total = time_total + value
time_avg = time_total / 10
print(times)
print(time_avg)


