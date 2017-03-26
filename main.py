from datetime import datetime
import eng_movies_provider as engAPI
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


def main():
	# capture current time
	startTime = datetime.now()
	print "[INFO] Starting The App"
	url = 'http://www.sharinggalaxy.com/14/ToServer.jsp?type=em&server=three'	
	obj = engAPI.eng_movies_provider()
	obj.set_url(url)
	obj.scrape()
	op = 'y'

	while(op!='n'):		
		search_string = raw_input("Enter Search string - ")
		result = obj.search(search_string)
		print "[INFO] SEARCHING for the movie "+ search_string
		# print result
		# print result['movie_list']
		if result['status']:
			for item in result['movie_list']:
				for key,value in item.items():
					get_all_links(value)
					# print key+" : "+value
		op = raw_input("Do you Want to Search More(y/n)?[Defaut: y]  ")

	print datetime.now()-startTime

if __name__ == '__main__':
	main()