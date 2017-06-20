from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from queue import Queue
from threading import Thread, Lock
from time import time, sleep
import http.cookiejar
import requests
import random
import json
import os
import re
import sys


class Reddit:
	"""A scraper for UofT's Course Finder web service.

	Course Finder is located at http://coursefinder.utoronto.ca/.
	"""

	host = 'https://www.reddit.com'
	#first_page_url = 'https://www.reddit.com/r/UofT/search?rank=title&q=timestamp%3A1455056765..1473005565&restrict_sr=on&syntax=cloudsearch'
	headers = {
		'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) '
		+ 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
	}

	def get_urls():
		nxt_time = 1119639970 # 2005/06/23
		urls = []

		while nxt_time < time():
			now_time = nxt_time
            # three months: 7776000
			# two months: 1728000
			# one month: 864000
			nxt_time = nxt_time + 864000
			url = 'https://www.reddit.com/r/UofT/search?rank=title&q=timestamp:' + str(now_time) + '..' + str(nxt_time) + '&restrict_sr=on&syntax=cloudsearch'
			urls.append(url)
		return urls

	start_urls = get_urls()
	cookies = http.cookiejar.CookieJar()
	threads = 100

	page_count = 1

	@staticmethod
	def get_html(url):
		if url.find('www.reddit') == -1:
			url = 'https://www.reddit.com' + url
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
		r = requests.get(url, headers=headers)
		text = r.text.encode('utf-8').decode('ascii', 'ignore')
		t = random.randint(1, 50)
		sleep(t/50)
		return text

	@staticmethod
	def scrape(location='.'):
		"""Update the local JSON files for this scraper."""

		Scraper.logger.info('Reddit initialized.')

		url_count = 1

		ts = time()
		queue = Queue()

		for x in range(Reddit.threads):
			worker = QandAFinderWorker(queue)
			worker.daemon = True
			worker.start()

		for url in Reddit.start_urls:
			next_page_url = url
			# page_count = 1
			while True:
				html = Reddit.get_html(next_page_url)
				idAndUrls = Reddit.search(html)
				next_page_url = Reddit.next_page(html)
				for idAndUrl in idAndUrls:
					queue.put(idAndUrl)
					url_count += 1
					Scraper.logger.info('Adding %dth url.' % url_count)
				if not next_page_url:
					break
                # else:
                #     print(page_count)
                #     page_count += 1
                #     print(next_page_url)

		queue.join()
		Scraper.logger.info('Took %.2fs to retreive reddit info.' % (
			time() - ts
		))

		Scraper.save_json(QandAFinderWorker.all_QandAs, location, 'QandAs')
		print("finished")

		Scraper.logger.info('Reddit completed.')

	@staticmethod
	def search(html):
        # headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        # r = requests.get(url, headers=headers)
        # text = r.text.encode('utf-8').decode('ascii', 'ignore')
		soup = BeautifulSoup(html, 'html.parser')

		links = []
		if soup.select('div.search-result.search-result-link') == []:
			return links
		div = soup.select('div.search-result.search-result-link')
		for item in div:
			title = item.div.header.a.get_text()
            # if not re.search('\?', title):
            #     continue
			fullname = item['data-fullname']
			link = item.div.header.a.get('href')
            # info = (fullname, link)
			links.append(link)
		return links

	@staticmethod
	def next_page(html):
        # headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        # r = requests.get(url, headers=headers)
        # text = r.text.encode('utf-8').decode('ascii', 'ignore')
		soup = BeautifulSoup(html, 'html.parser')

		if len(soup.select('span.nextprev a')) > 0:
			nxt_link = soup.select('span.nextprev a')[-1]
			if nxt_link['rel'][1] == 'next':
				return nxt_link['href']
			else:
				return None
		else:
			return None

	@staticmethod
	def parse_course_html(html):
		# !!!Can use a helper function to save the soup
		soup = BeautifulSoup(html, 'html.parser')
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
		if len(answer.split()) > 30:
			return
		QandA = {'question': question, 'answer': answer}
		return QandA


class QandAFinderWorker(Thread):

    all_QandAs = []
    done = 0
    lock = Lock()

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            html = Reddit.get_html(url)
            QandA = Reddit.parse_course_html(html)
            if QandA:
                QandAFinderWorker.lock.acquire()
                QandAFinderWorker.all_QandAs.append(QandA)
                QandAFinderWorker.done += 1
                Scraper.flush_percentage(QandAFinderWorker.done / 1000)
                QandAFinderWorker.lock.release()

            self.queue.task_done()
