import re
import urllib
import urlparse
from bs4 import BeautifulSoup

url = "http://58.65.128.2:602/English%20Movies%20(H%20-%20L)/Harry%20Potter-1-2-3-4-5-6-7/?sortby"

def get_all_links(url):
	html = urllib.urlopen(url)
	bs = BeautifulSoup(html.read(),"lxml")

	#find the no of available links
	all_links = bs.findAll("a",href= re.compile('^\/English Movies*'))

	for link in all_links:
		#print link.text +" ==> "+ link['href']
		url_obj = urlparse.urlparse(url)
		base_url = "http://"+url_obj.netloc
		if ".avi" in link['href'] or ".mp4" in link['href'] or ".flv" in link['href'] or ".mkv" in link['href']:
			print link.text +" ==> "+ base_url+link['href']

		else:
			directory_url = base_url+link['href']
			# print "Directory Found -- " + directory_url
			get_all_links(directory_url)

get_all_links(url)
