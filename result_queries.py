import psycopg2
con = psycopg2.connect(user="admin", password="admin", host = "127.0.0.1",port = "5432",database="comparator")
cursor = con.cursor()


#no_queries = 8
#put all queries here;add a description for each query
def execute_query(query,description):
	cursor.execute(query)
	con.commit()
	result = cursor.fetchall()
	return description, result

def read_in_queries():
	results = []
	read_file = open("query_file.txt","r")
	queries = read_file.readlines()
	x = 0
	for line in queries:
		if x % 2 == 0:
			description = line
		else:
			query = line
			description, result = execute_query(query,description)
			results.append([description,result])
		x = x + 1
	output_queries(results)

def output_queries(results):
	open("output_results.csv","w").close()
	output_file = open("output_results.csv","a")
	for part in results:
		#print(part[1])
		if len(part[1]) == 0:
			#print("EMPTY",part)
			empty_tuple = (' ',' ')
			part[1].append(empty_tuple)
			#print(part[1])
	print(results)
	print(results[0][1][0][0])
	data_to_write = "total number of domains,"+str(results[0][1][0][0])+"\n"+"blocked by quad 9,"+str(results[1][1][0][0])+"\nblocked by quad9_noblock,"+str(results[2][1][0][0])+"\nblocked by google,"+str(results[3][1][0][0])+"\nblocked by cloudflare safe,"+str(results[4][1][0][0])+"\nblocked by cloudflare,"+str(results[5][1][0][0])+"\nblocked by opendns," +str(results[6][1][0][0])+"\nblocked by ultrarecursive,"+str(results[7][1][0][0])+"\n\n , ,number of domains blocked\nsource name, total number of domains, quad_9,quad9_noblock,google,cloudflare_safe,cloudflare,opendns,ultrarecursive\n"
	source_array = []
	print(str(results[16][1][0]))
	for source in results[16][1]:
		print("source",source)
		source_one = []
		source_one.append(str(source[0]))
		source_one.append(str(source[1]))	
		source_array.append(source_one)
	print("source_array",source_array)
	
	for domain in results[17][1]:
		print("DOMAIN1",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 3:
			part.append("0")
			
	for domain in results[18][1]:
		print("DOMAIN2",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 4:
			part.append("0")
	for domain in results[19][1]:
		print("DOMAIN3",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 5:
			part.append("0")
	for domain in results[20][1]:
		print("DOMAIN4",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 6:
			part.append("0")
	for domain in results[21][1]:
		print("DOMAIN5",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 7:
			part.append("0")
	for domain in results[22][1]:
		print("DOMAIN6",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 8:
			part.append("0")
	for domain in results[23][1]:
		print("DOMAIN7",domain)
		for section in source_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in source_array:
		if len(part) != 9:
			part.append("0")
	print("SOURCE_ARRAY",source_array)
	for value in source_array:
		print("an output line",value)
		output_string = str(value[0])+","+str(value[1])+","+str(value[2])+","+str(value[3])+","+str(value[4])+","+str(value[5])+","+str(value[6])+","+str(value[7])+","+str(value[8])+"\n"
		data_to_write = data_to_write + output_string

	column_titles = "\n , ,number of domains blocked\n top level domain, total number of domains, quad_9,quad9_noblock, google,cloud flare safe, cloud flare,opendns, ultra_recursive\n"
	data_to_write = data_to_write + column_titles

	domain_array = []
	for domain in results[8][1]:
		domain_one = []
		domain_one.append(str(domain[0]))
		domain_one.append(str(domain[1]))
		domain_array.append(domain_one)
	for domain in results[9][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 3:
			part.append("0")
	for domain in results[10][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 4:
			part.append("0")
	for domain in results[11][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 5:
			part.append("0")
	for domain in results[12][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 6:
			part.append("0")
	for domain in results[13][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 7:
			part.append("0")
	for domain in results[14][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 8:
			part.append("0")

	for domain in results[15][1]:
		for section in domain_array:
			if section[0] == domain[0]:
				section = section.append(domain[1])
	for part in domain_array:
		if len(part) != 9:
			part.append("0")
	for value in domain_array:
		output_string = str(value[0])+","+str(value[1])+","+str(value[2])+","+str(value[3])+","+str(value[4])+","+str(value[5])+","+str(value[6])+","+str(value[7])+","+str(value[8])+"\n"
		data_to_write = data_to_write + output_string
	output_file.write(data_to_write)
	output_file.write("Additional queries:\n")
	for x in range(24,len(results)):
		text = str(results[x][0]) + "," + str(results[x][1]) + "\n"
		output_file.write(text)

read_in_queries()
	


