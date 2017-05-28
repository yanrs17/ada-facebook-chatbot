from bs4 import BeautifulSoup
import urllib
from Queue import Queue
import re
import time

def parse_comment_page(url):
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'lxml')
	
	#print soup.select('div.expando div.md')
	post_content = soup.select('div.expando div.md')[0].get_text()
	if len(str(content_post.get_text()).split()) > 60:
			return

	question = soup.select('p.title a.title.may-blank')[0].get_text()
	top = soup.select('div.commentarea div.md')[0]
	answer = top.select('p')[0].get_text()

	QandA = OrderedDict([
		('question', question),
		('answer', answer)
	])

	return QandA

def parse_html(url):
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'lxml')
	links = []
	titles = []

	time.sleep(7)
	html_lst = soup.select('a.title.may-blank')
	for e in html_lst:
		title = e.get_text()
		if not re.search('\?', title):
			continue
		links.append(e['href'])

	# nxt_link = soup.select('span.next-button a')[0]['href']
	# parse_html(nxt_link)
	#print soup.find_all('span', class_ = 'next-button')

parse_html('https://www.reddit.com/r/UofT')