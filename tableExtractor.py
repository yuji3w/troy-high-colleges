import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import argparse
import operator
import os
import collections
from collections import Counter

http = httplib2.Http()
status, response = http.request("https://troychariot.org/3227/news/the-2018-college-list/")

soup = BeautifulSoup(response, "html.parser")

# from https://stackoverflow.com/a/23377804

data = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
	cols = row.find_all('td')
	cols = [ele.text.strip() for ele in cols]
	data.append([ele for ele in cols if ele]) # Get rid of empty values

#pprint(data)


tempdata = []
unis = []

data.pop(0) # removes labels [First, Last Name, Uni] from data
for person in data:
	name = person[0] + " " + person[1]
	uni = person[2]
	unis.append(uni)
	tempdata.append([name, uni])
data = tempdata

unisDict = Counter(unis)

orderedUnis = [(k, unisDict[k]) for k in sorted(unisDict, key=unisDict.get, reverse=True)]
for uni in orderedUnis:
	if "Working full time" in uni[0] or "Undecided" in uni[0]:
		if uni[1] is 1:
			print(str(uni[1]) + " Troy High School student is " + uni[0].lower() + ".")
		else:
			print(str(uni[1]) + " Troy High School students are " + uni[0].lower() + ".")
	elif uni[1] is 1:
		print(str(uni[1]) + " Troy High School student attends " + uni[0] + ".")
	else:
		print(str(uni[1]) + " Troy High School students attend " + uni[0] + ".")
