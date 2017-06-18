from bs4 import BeautifulSoup
import requests
import urllib
import json
from Queue import Queue
import re
import time

def parse_comment_page(url):
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	r = requests.get(url, headers=headers)
	text = r.text.encode('utf-8').decode('ascii', 'ignore')
	#!!!Can use a helper function to save the soup
	soup = BeautifulSoup(r.text, 'html.parser')

	if soup.select('div.expando div.md') == []:
		return
	post_content = soup.select('div.expando div.md')[0].get_text()
	if len(str(post_content).split()) > 70:
			return
	if soup.select('p.title a.title.may-blank') == []:
		return
	question = soup.select('p.title a.title.may-blank')[0].get_text()

	if soup.select('div.commentarea div.md') == []:
		return
	top = soup.select('div.commentarea div.md')[0]
	if top.select('p') == []:
		return
	answer = top.select('p')[0].get_text()

	# QandA = OrderedDict([
	# 	('question', question),
	# 	('answer', answer)
	# ])
	QandA = {'question':question, 'answer':answer}
    print QandA
    return QandA

#parse_comment('https://www.reddit.com/r/UofT/comments/6ebds6/where_to_find_information_about_the_social/')
#parse_comment('https://www.reddit.com/r/UofT/comments/6e8kkg/coming_for_exchange_in_toronto_but_this_timetable/')

def next_page(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    r = requests.get(url, headers=headers)
    text = r.text.encode('utf-8').decode('ascii', 'ignore')
    soup = BeautifulSoup(r.text, 'html.parser')

    if len(soup.select('span.nextprev a')) == 1:
		nxt_link = soup.select('span.nextprev a')[0]['href']
		#print nxt_link
		return nxt_link
	elif len(soup.select('span.nextprev a')) > 1:
		nxt_link = soup.select('span.nextprev a')[1]['href']
		#print nxt_link
		return nxt_link
	else:
		return None

def search(url):
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	r = requests.get(url, headers=headers)
	text = r.text.encode('utf-8').decode('ascii', 'ignore')
	soup = BeautifulSoup(r.text, 'html.parser')

	links = []
	if soup.select('div.search-result.search-result-link') == []:
		return None
	div = soup.select('div.search-result.search-result-link')
	for item in div:
		title = item.div.header.a.get_text()
		if not re.search('\?', title):
			continue
		fullname =  item['data-fullname']
		link = item.div.header.a.get('href')
		info = (fullname, link)
		links.append(info)
	return links

#parse_comment_page('https://www.reddit.com/r/UofT/comments/6e6z6q/utm_shuttle_bus_timetable_incorrect/')
#next_page('https://www.reddit.com/r/UofT/search?rank=title&q=timestamp%3A1455056765..1473005565&restrict_sr=on&syntax=cloudsearch')
#next_page('https://www.reddit.com/r/UofT/search?rank=title&q=timestamp%3A1455056765..1473005565&restrict_sr=on&syntax=cloudsearch&count=25&after=t3_48pgty')

"""
!!! need to change the first_page_url to https://www.reddit.com/r/UofT/search?rank=title&q=timestamp%3A1455056765..1473005565&restrict_sr=on&syntax=cloudsearch
"""
search('https://www.reddit.com/r/UofT/search?rank=title&q=timestamp%3A1455056765..1473005565&restrict_sr=on&syntax=cloudsearch')
