from .scraper import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from Queue import Queue
from threading import Thread, Lock
from time import time, sleep
import cookielib
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
    first_page_url = 'https://www.reddit.com/r/UofT/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    cookies = cookielib.CookieJar()
    threads = 32

    page_count = 1

    @staticmethod
    def get_html(url):
        if url.find('www.reddit') == -1:
            url = 'https://www.reddit.com' + url
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        r = requests.get(url, headers=headers)
        text = r.text
        #text = r.text.encode('utf-8').decode('ascii', 'ignore')
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

        next_page_url = Reddit.first_page_url
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

        queue.join()

        Scraper.logger.info('Took %.2fs to retreive reddit info.' % (
            time() - ts
        ))

        Scraper.save_json(QandAFinderWorker.all_QandAs, location, 'QandAs')

        Scraper.logger.info('Reddit completed.')

    @staticmethod
    def search(html):
        html = BeautifulSoup(html, 'html.parser')
        links = []
        ids = []
        html_lst = html.select('div.entry.unvoted a.title.may-blank')
        id_lst = html.select('div.linkflair')
        has_id_index = []
        id_link_tuples_lst = []
        for j in range(len(html_lst)):
            title = html_lst[j].get_text()
            if not re.search('\?', title):
                continue
            has_id_index.append(j)
            if html_lst[j]['href'].find('/r/UofT') == -1:
                print('useless link %s', html_lst[j]['href'])
                continue
            links.append(html_lst[j]['href'])
        # print html_lst
        # print "Links on current page : "
        # print id_link_tuples_lst
        return links

    @staticmethod
    def next_page(html):
        html = BeautifulSoup(html, 'html.parser')
        if len(html.select('span.next-button a')) > 0:
            nxt_link = html.select('span.next-button a')[0]['href']
        # print "Next link: "
        # print nxt_link
            #print(Reddit.page_count)
            #print(nxt_link)
            Reddit.page_count += 1
            return nxt_link
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

