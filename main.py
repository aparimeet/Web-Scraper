import threading
from queue import Queue
from TheSpider import Spider
from get_domain import *
from general import *

PROJECT_NAME = 'webcrawler'
HOMEPAGE = 'https://thenewboston.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()         #Thread queue
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


#If there are items in queue, crawl them
def crawl():
    queued_links = fileToSet(QUEUE_FILE)
    if len(queued_links) > 0 :
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

#Each queued link is a new job
def create_jobs():
    for link in fileToSet(QUEUE_FILE):
        queue.put(link)
    queue.join()    #Make sure the threads dont bump into each other
    crawl()

#Creates spider threads. They terminate when main exits    
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = Threading.Thread(target = work)     #work = next job in queue
        t.daemon = True                 #Daemon is computer program that runs in background
        t.start()

#Defines the next job in queue
def work():
    while True:
        url = queue.get()
        Spider.crawlPage(threading.current_thread().name, url)
        queue.task_done()
    
