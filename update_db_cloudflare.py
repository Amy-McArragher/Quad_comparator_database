import psycopg2
import dns
import dns.resolver
import dns.rcode
con = psycopg2.connect(user="admin", password="admin", host = "127.0.0.1",port = "5432",database="comparator")
cursor = con.cursor()
input_file = open("input_cloudflare.txt","r")
input_domains = input_file.read()
input_domains = input_domains.split(" ")
#domains = tuple(input_domains)
query_update = "UPDATE results SET cloudflare_safe = '0' WHERE domain = %s;"
for domain in input_domains:
	cursor.execute(query_update,(domain,))
con.commit()
