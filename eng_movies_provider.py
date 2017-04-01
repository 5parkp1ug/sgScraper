import re
import urllib
from bs4 import BeautifulSoup
import unicodedata
import urlparse

class eng_movies_provider:
	"""docstring for eng_movies_provider"""
		
	def set_url(self, url):
		self.url = url
		self.level1_urls = {}
		self.level2_urls = {}

	def getSoup(self, url):
		try:
			html = urllib.urlopen(url)
		except IOError:
			return {
				"status": False,
				"message": "Please check your connectivity."
			}
		bs = BeautifulSoup(html.read(),"lxml")

		return {
			"status": True,
			"soup": bs
		}

	def getUrls(self):
		print "[INFO] Starting Scraping Level 1"
		response = self.getSoup(self.url)
		if response['status']:
			bs = response['soup']
		else:
			return response
		level1_tags = bs.findAll("a",{"class":"button"})
		print "[RESULT] %d URLs found"%(len(level1_tags))
		for tag in level1_tags:
			range_text = unicodedata.normalize('NFKD', tag.text).encode('ascii','ignore').replace(" ","")
			range_url = tag["href"]
			# level1_urls[range_text] = range_url
			self.scrape_level2(range_url)
		return self.level2_urls

	def scrape_level2(self, range_url):
		print "[INFO] Starting Scraping Level 2"
		#find the sub-categorization in the page and get their url
		response = self.getSoup(range_url)
		if response['status']:
			bs = response['soup']
		else:
			return response

		no_of_links = bs.findAll("a",href= re.compile('^\/English*'))
		print "[RESULT] %d URLs found"%(len(no_of_links))
		for item in no_of_links:
			movie_range = item.text.strip("English Movies ").strip("(").strip(")").replace(" ","")
			movie_range_url = range_url + item['href'][1:].replace(" ","%20")
			# print movie_range +" --> "+ movie_range_url
			self.level2_urls[movie_range] = movie_range_url

		return self.level2_urls