
import dns
import dns.resolver
import dns.rcode
import csv
import datetime
import socket
domains_to_update = []
input_file = open("output_opendns.txt","r")
domains = input_file.readline()
#domains = domains.strip(')')
#domains = domains.strip('(')
domains = domains.split(",")
resolver = dns.resolver.Resolver()
#resolver.nameservers = ['208.67.222.222']
for domain in domains:
	if domain == ")":
		continue
	domain = str(domain)
	domain = domain.replace("'","")
	domain = domain.replace("(","")
	try:
		code = resolver.query(domain).response.rcode()
		if str(code) == '0':#resolved
			print("no")
			
		else:
			print(domain," update")
			domains_to_update.append(domain)
	except:
		print(domain," update")
		domains_to_update.append(domain)
print(domains_to_update)
output_file = open("input_opendns.txt","w")
for domain in domains_to_update:
	output_file.write(domain)

