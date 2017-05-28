from bs4 import BeautifulSoup
from collections import OrderedDict
from queue import Queue
from threading import Thread, Lock
import json
import os
import re
import sys

class Courses:
	start_url = 'https://www.reddit.com/r/UofT/'
	threads = 32

	@staticmethod
	def scrape():
		queue = Queue()
		#TODO

class CommentFinder(Thread):
	lock = Lock()

	def __init__(self, queue):
    	Thread.__init__(self)
    	self.queue = queue

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

    def run(self):
    	while True:
    		url = queue.get()
    		#pair = parse_comment_page(url)

    		CommentFinder.lock.acquire()
    		CommentFinder.lock.release()

    		self.queue.task_done()

class htmlFinder(Thread):
	lock = Lock()

	def __init__(self, queue):
    	Thread.__init__(self)
    	self.queue = queue

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

parse_html('https://www.reddit.com/r/UofT')

    def run(self):
    		
    	#parse_html()
    	CommentFinder.lock.acquire()
    	CommentFinder.lock.release()

    	self.queue.task_done()

