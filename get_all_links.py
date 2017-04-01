import re
import urllib
from datetime import datetime
from urlparse import urlparse
from bs4 import BeautifulSoup

url = "http://58.65.128.2:602/English%20Movies%20(H%20-%20L)/?sortby="
# url = "http://58.65.128.2:603/English Movies (S - T)/War Dogs 2016 HDTS?sortby="
result = []
def get_all_movies(url):
	response = {}
	o = urlparse(url)
	base_url = o.netloc
	html = urllib.urlopen(url)
	bs = BeautifulSoup(html.read(),"lxml")

	#find the no of available links
	all_links = bs.findAll("tr",style = False)

	for link in all_links:
		full_url = "http://"+base_url+link.td.next.next.next.a['href']
		full_url = full_url.encode("utf-8").lower()
		movie_name = link.td.next.next.next.a.getText()
		if "." not in movie_name and "xampp" not in movie_name:
			print "Directory: " + link.td.next.next.next.a.getText()
			get_all_movies(full_url)
		elif ".m4v" in full_url or ".rm" in full_url or ".mov" in full_url or ".wmv" in full_url or ".divx" in full_url or ".rmvb" in full_url or ".vob" in full_url or ".avi" in full_url or ".mp4" in full_url or ".flv" in full_url or ".mkv" in full_url or ".zip" in full_url or ".dat" in full_url or ".rar" in full_url:
			response = {
				'url' : full_url,
				'name': movie_name
			}

			print response
			result.append(response)
			print "===================================="
		elif ".srt" in full_url or ".sub" in full_url:
			#subtitle found do something
			pass
		elif ".mpg" in full_url or ".mht" in full_url or ".jpeg" in full_url or ".jpg" in full_url:
			pass
