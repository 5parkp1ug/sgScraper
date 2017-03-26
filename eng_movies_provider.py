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

	def scrape(self):
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

	def search(self, param):
		print "[STATUS] Starting URL Search module"
		response = {
			"status": False,
			"message": "Please run the scrape module first."
		}
		if self.level2_urls:
			first_letter = param[0]
			for key, value in self.level2_urls.items():
				#search for movie in the respective range URL
				if first_letter >= key.split("-")[0] and first_letter <= key.split("-")[1]:
					print "[RESULT] Found the URL to search for the movie - "+ value
					response = {
						"status": True,
						"movie_list": self.get_movie_url(param, value) 
					}
					return response
			response["message"] = "Invalid input."
			return response
		else:
			return response

	def get_movie_url(self, name, range_url):
		print "[STATUS] Starting Movie search Module"
		regex = ""
		#create the keyword from the name of the movie
		keywords = name.split()
		print "[INFO] keywords to search are - "+ str(keywords)
		for name in keywords:
			regex += "(?=.*\\b"+name+"\\b)" 
		print "[INFO] Regex to search is - "+ regex
		response = self.getSoup(range_url)
		if response['status']:
			bs = response['soup']
			all_movies = bs.findAll("a",{'href' : re.compile('^'+regex+'.*$')})
			# all_movies = bs.findAll("href" = keywords)
			return [{a.text: range_url.strip("?sortby=")+"/"+a['href'].split("/")[2].replace(" ", "%20")} for a in all_movies]

		else:
			return response


			
