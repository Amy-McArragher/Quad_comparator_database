from urllib.request import urlopen

def get_file(url,filename):
	page = urlopen(url)
	html_bytes = page.read()
	html = html_bytes.decode("utf-8","replace")
	file = open(filename,"w",encoding="utf8")
	file.write(html)
	file.close()

get_file("https://osint.digitalside.it/Threat-Intel/lists/latesturls.txt","Digitalside.txt")
get_file("http://data.phishtank.com/data/online-valid.csv","Phishtank.txt")
get_file("https://rescure.me/rescure_domain_blacklist.txt","Rescure_domain.txt")
get_file("https://rescure.me/covid.txt","Covid.txt")
get_file("https://openphish.com/feed.txt","Feed.txt")


