from multiprocessing import Pool
from datetime import datetime
import eng_movies_provider as engAPI
from get_all_links import get_all_movies as getAllMovies
import re
import urllib
import urlparse
from bs4 import BeautifulSoup


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
	all_links = [value for value in obj.getUrls().values()]
	
	# Single thread
	# for key,value in all_links.items():
	# 	print "getting all links for " + value
	# 	getAllMovies(value)
	

	#Using Pool
	p = Pool()
	p.map(getAllMovies,all_links)
	p.close()
	p.join()




	print datetime.now()-startTime

if __name__ == '__main__':
	main()