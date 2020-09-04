#!/usr/bin/env python3

#apt install python3-pip
#pip3 install dnspython
import psycopg2
import os, sys
import dns
import dns.resolver
import dns.rcode
import re
import time
import executor
import concurrent.futures
import argparse
from threading import Thread
from queue import Queue
import csv
import datetime
import socket
import decimal
con = psycopg2.connect(user="admin", password="admin", host = "127.0.0.1",port = "5432",database="comparator")
cursor = con.cursor()
#resolved = 1
#not resolved = 0

def dns_resolver(url,con,cursor):
	global total_count
	global resolved_quad
	global resolved_google
	global resolved_cloud_safe
	global resolved_cloud
	global resolved_opendns
	global resolved_quad9_noblock
	global resolved_ultrarecursive
	resolver = dns.resolver.Resolver()
	total_count += 1
	quad9 = None
	google = None
	cloud_safe = None
	cloud = None
	opendns = None
	quad9_noblock = None
	ultrarecursive = None
	quad9_time = None
	google_time = None
	cloud_safe_time = None
	cloud_time = None
	opendns_time = None
	quad9_noblock_time = None
	ultrarecursive_time = None
	#regex = r"(?i)\b(?:(?:https?|ftp|file)^:\/\/|[-A-Z0-9]{1,60}\.)(?:\([-A-Z0-9+&@#%=~_|$?!:,.]*\)|[-A-Z0-9+&@#%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#%=~_|$?!:,.]*\)|[A-Z0-9+&@#%=~_|$])"
	exist = True
	try:
		socket.gethostbyname(url)
	except socket.gaierror:
		exist = False
		print("Domain does not exist",url)
		query = "UPDATE Domains SET registrar = 'Does not exist' WHERE domain = %s"
		cursor.execute(query,(url,))
		con.commit()
		#run this seperately so it doesnt slow it all down
	if exist == True:
		try:
			resolver.nameservers = ['9.9.9.9']
			#domain = re.search(regex, url).group()
			domain = url
			start = time.process_time()
			code = resolver.query(domain).response.rcode()
			quad9_time = time.process_time() - start
			if str(code) == '0':
				quad9 = '1'
				resolved_quad += 1
			else:
				quad9 = '0'
		except:
			quad9 = '0'

		try:
			resolver.nameservers = ['9.9.9.10']#changed from 1.1.1.1
			domain = url
			start = time.process_time()
			code = resolver.query(domain).response.rcode()
			quad9_noblock_time = time.process_time() - start
			if str(code) == '0':
				quad9_noblock = '1'
				resolved_quad9_noblock += 1
			else:
				quad9_noblock = '0'
		except:
			quad9_noblock = '0'

			
		try:
			resolver.nameservers = ['8.8.8.8']
			domain = url
			start = time.process_time()
			code = resolver.query(domain).response.rcode()
			google_time = time.process_time() - start
			if str(code) == '0':
				google = '1'
				resolved_google += 1
			else:
				google = '0'
		except:
			google = '0'
			

		try:
			resolver.nameservers = ['1.1.1.2']
			domain = url
			start = time.process_time()
			#cloudflare does not currently support DNS-over-TLS so currently using UDP
			#once TLS works with the cloudflare safe search this will need to be changed
			code = resolver.query(domain).response.rcode()
			cloud_safe_time = time.process_time() - start
			if str(code) == '0':
				cloud_safe = '1'
				resolved_cloud_safe += 1
			else:
				cloud_safe = '0'
		except:
			cloud_safe = '0'

		try:
			resolver.nameservers = ['1.1.1.1']
			domain = url
			start = time.process_time()
			code = resolver.query(domain).response.rcode()
			cloud_time = time.process_time() - start
			if str(code) == '0':
				cloud = '1'
				resolved_cloud += 1
			else:
				cloud = '0'
		except:
			cloud = '0'

		try:
			resolver.nameservers = ['208.67.222.222']
			domain = url
			code = resolver.query(domain).response.rcode()
			opendns_time = time.process_time() - start
			if str(code) == '0':
				opendns = '1'
				resolved_opendns += 1
			else:
				opendns = '0'
		except:
			opendns = '0'

		try:
			resolver.nameservers = ['156.154.70.2']#this is ultra recursive
			domain = url
			start = time.process_time()
			code = resolver.query(domain).response.rcode()
			ultrarecursive_time = time.process_time() - start
			if str(code) == '0':
				ultrarecursive = '1'
				resolved_ultrarecursive += 1
			else:
				ultrarecursive = '0'
		except:
			ultrarecursive = '0'
			
		i = str(domain)+','+str(quad9)+','+str(quad9_noblock)+','+str(google)+ ',' + str(cloud_safe) + ',' + str(cloud) + ',' + str(opendns) + ',' + str(ultrarecursive)+','+str(domain)+','+str(quad9_time)+','+str(quad9_noblock_time)+','+str(google_time)+ ',' + str(cloud_safe_time) + ',' + str(cloud_time) + ',' + str(opendns_time) + ',' + str(ultrarecursive_time)+',\n'
		queue.put(i)


def process_threads(maxthreads,con,cursor,source_name):
	#open file and load into array
	#loading into an array works for when the database is this size but may cause an
	#overflow error when it gets bigger, so we will have to consider loading the domains in
	# a chunk at a time.
	query = "SELECT domains.domain FROM Domains JOIN sources on sources.domain = domains.domain WHERE sources.source = %s"#WHERE WHERE CAST(created_at AS DATE) = CURRENT_DATE"
	print(source_name)
	cursor.execute(query,(source_name,))
	con.commit()
	#url_list = []
	urls = cursor.fetchall()
	#for url in urls:
	#	print(url)
	consumer = Thread(target=consume,args=(con,cursor,))
	consumer.setDaemon(True)
	consumer.start()
	#create threads using concurrent.futures
	#this runs n threads, waits until they finish and runs another n until finish
	executor = concurrent.futures.ThreadPoolExecutor(maxthreads)
	futures = [executor.submit(dns_resolver, url[0],con,cursor) for url in urls]
	concurrent.futures.wait(futures)
	#sleep to ensure all threads are finished
	time.sleep(5)
	global finished_processing
	finished_processing = True
	time.sleep(5)
	global resolved_quad
	global resolved_google
	global resolved_cloud_safe
	global resolved_cloud
	global resolved_opendns
	global resolved_quad9_noblock
	global resolved_ultrarecursive
	#print stats
	print('Total Stats')
	print('Total Domains: ', total_count)
	print('Total Blocked:')
	print('Quad9:', total_count - resolved_quad)
	print('quad9_noblock:', total_count - resolved_quad9_noblock)
	print('Google:', total_count - resolved_google)
	print('cloudflare safe:', total_count - resolved_cloud_safe)
	print('cloudflare:',total_count - resolved_cloud)
	print('opendns:', total_count - resolved_opendns)
	print('ultrarecursive:', total_count - resolved_ultrarecursive)
	

def consume(con,cursor):
	date = datetime.date.today()
	date = str(date)
	global finished_processing
	while finished_processing != True:
		if not queue.empty():
			input_list = []
			i = queue.get()
			i = i.strip()
			i = i[:-1]
			#print(i)
			#i = i.replace("Not resolved","0")
			#i = i.replace("Resolved","1")
			input_list = i.split(",")
			#print("INPUT_LIST",input_list)
			result_list = input_list[:8]
			result_list.insert(0,date)
			query = "INSERT INTO Results VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"#may need an extra input
			cursor.execute(query,result_list)
			con.commit()
			#print(result_list)
			time_list = input_list[-8:]
			time_list_dec = []
			time_list_dec.append(time_list[0])
			time_list.pop(0)
			#print("TIME LIST",time_list)
			for value in time_list:
				if value == "None":
					value = "0"
				#print("VALUE",value)
				value_dec = decimal.Decimal(value)
				time_list_dec.append(value_dec)
			time_list_dec.insert(0,date)
			#print(time_list_dec)
			#print(time_list)
			query = "INSERT INTO Resolve_time VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"#may need an extra input
			cursor.execute(query,time_list_dec)
			con.commit()

	return


def main(con,cursor,source_name):
	print("Running comparator")
	global total_count
	global resolved_quad
	global resolved_google
	global resolved_cloud_safe
	global resolved_cloud
	global resolved_opendns
	global resolved_quad9_noblock
	global resolved_ultrarecursive
	global finished_processing
	global queue
	queue = Queue()
	total_count = 0
	resolved_quad = 0
	resolved_google = 0
	resolved_cloud_safe = 0
	resolved_cloud = 0
	resolved_opendns = 0
	resolved_quad9_noblock = 0
	resolved_ultrarecursive = 0
	finished_processing = False
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--threads", type=int, default=6, help="Select number of threads. Default 4")
	args = parser.parse_args()
	maxthreads = args.threads
	process_threads(maxthreads,con,cursor,source_name)





#TODO
#look into reducing memory allocation amount (incremental file reads)

