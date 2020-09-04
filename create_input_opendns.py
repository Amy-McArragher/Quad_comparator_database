import psycopg2
import dns
import dns.resolver
import dns.rcode
output_file = open("output_opendns.txt","w")
con = psycopg2.connect(user="admin", password="admin", host = "127.0.0.1",port = "5432",database="comparator")
cursor = con.cursor()
query = "SELECT domain FROM results WHERE results.created_at = CURRENT_DATE AND opendns = '1';"
cursor.execute(query)
domains = cursor.fetchall()
output_file.write(str(domains))


