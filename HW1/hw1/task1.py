from bs4 import BeautifulSoup
from time import sleep
import time
import requests
from random import randint
from html.parser import HTMLParser
import json

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
searching_url='https://html.duckduckgo.com/html/?q='
class SearchEngine:
	@staticmethod
	def search(query, sleep=True):
		if sleep: # Prevents loading too many pages too soon
			sleeptime = randint(10, 100)
			print("sleep for "+ str(sleeptime) +" seconds.")
			time.sleep(sleeptime)
		temp_url = '+'.join(query.split()) #for adding + between words for the query
		url = searching_url + temp_url
		#print(url)
		soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text,"html.parser")
		#print(soup)
		new_results = SearchEngine.scrape_search_result(soup)
		return new_results
	@staticmethod
	def scrape_search_result(soup):
		raw_results = soup.find_all("a", attrs = {"class" : "result__a"})
		results = []
		#implement a check to get only 10 results and also check that URLs must not be duplicated
		for result in raw_results:
			link = result.get('href')
			results.append(link)
		return results

def writeJson(dictionary):
  # Serializing json
	json_object = json.dumps(dictionary, indent=4)
	# Writing to sample.json
	with open("hw1.json", "w") as outfile:
		outfile.write(json_object)
def readJson():
  with open('hw1.json', 'r') as openfile:
    json_object = json.load(openfile)
    return json_object
  
resJSON={}
queries = []
with open('100QueriesSet4.txt') as f:
	while(True):
		line = f.readline()
		if(line):
			line = line[:-2]
			queries.append(line)
		else:
			break
f.close()
queries0 = queries[0:1]
queries1 = queries[0:25]
queries2 = queries[25:50]
queries3 = queries[50:75]
queries4 = queries[75:100]
for queryStr in queries4:
  resJSON=readJson()
  result = SearchEngine.search(queryStr,sleep=True)
  result= list(dict.fromkeys(result))
  print(queryStr)
  print(len(result))
  resJSON[queryStr]=result[:10]
  #print(resJSON)
  writeJson(resJSON)
