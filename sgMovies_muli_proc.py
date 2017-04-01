import re
import urllib
import Queue
import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool, Value

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def scrape_level1(url):

	bs = BeautifulSoup(url.read(),"lxml")
	level1_tags = bs.findAll("a",{"class":"button"})

	for tag in level1_tags:
		level1_urls.append(tag["href"])
		scrape_level2(tag["href"])



def scrape_level2(url):

	#find the sub-categorization in the page and get their url
	html = urllib.urlopen(url)
	bs = BeautifulSoup(html.read(),"lxml")

	no_of_links = bs.findAll("tr",{"onclick":True})
	for link in no_of_links:
		path = link['onclick'].strip("window.location='/").strip("=';").strip("?sortby").replace(" ","%20")
		full_url = url+path
		level2_urls.append(full_url)

def init(counter):
	global moviectr
	moviectr = counter


def scrape_level3(full_url):

	print "calling scrape level 3"
	#find the name of the movies from the sub-categpry page
	html = urllib.urlopen(full_url)
	bs = BeautifulSoup(html.read(),"lxml")

	movies = bs.findAll("a",re.compile('^\/English*'))
	print len(movies)
	o = urlparse.urlparse(full_url)
	url = o.netloc
	for movie in movies:
		print bcolors.HEADER + "Movie Name - %s"%(movie.getText()) # Name of the movie
		level3_urls.append(movie.getText())
		moviectr+=1
		print moviectr
		#print bcolors.OKBLUE + "http://"+url+path

		# path = movie['href'].replace(" ","%20")
		# if path != '/':	
		# 	if "Harry" in "http://"+url+path:
		# 		print "http://"+url+path


##################################################################################
#Variables
level1_urls = []
level2_urls = []
level3_urls = []



# capture current time
startTime = datetime.now()

url = urllib.urlopen('http://www.sharinggalaxy.com/14/ToServer.jsp?type=em&server=three')
scrape_level1(url)
print level1_urls
print level2_urls

#create a Multiprocessing value for counter
moviectr = Value('i',1)
print moviectr
p = Pool(initializer=init, initargs=(moviectr,))
p.map(scrape_level3,level2_urls)


print moviectr

# print current time minus the start time
print datetime.now()-startTime