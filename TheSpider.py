from urllib.request import urlopen
from  linksFinder import linkFinder
from general import *

class Spider:
    
    #The following variables are shared between every spider
    #Creating multiple spiders helps to crawl the page faster. This is a multi-threaded program
    base_url = ''
    domain_url = ''     #To ensure we are accessing valid webpages without generating errors
    projectName = ''
    #The files are their respective sets have the same information, but while storing the links we use sets as they are faster and then when our work is done we transfer it to their files 
    queueFile = ''
    crawledFile = ''
    queue = set()
    crawled = set()

    def __init__(self, projectName, base_url, domain_url):
        Spider.base_url = base_url
        Spider.domain_url = domain_url
        Spider.projectName = projectName
        Spider.queueFile = Spider.projectName + '/queue.txt'
        Spider.crawledFile = Spider.projectName + '/crawled.txt'
        Spider.initiate()   #Initiates the spider
        Spider.crawlPage('Initial spider', Spider.base_url)

    @staticmethod
    def initiate():  #This is a static method as we do not make the use of self variable
        createProject(Spider.projectName)   
        create_queue_crawled(Spider.projectName, Spider.base_url)   #Creates the queue and crawled files
        Spider.queue = fileToSet(Spider.queueFile)      #Converts waiting list file to set
        Spider.crawled = fileToSet(Spider.crawledFile)  #Converts crawled file to set

    @staticmethod
    def crawlPage(threadName, page_url):
        if page_url not in Spider.crawled:
            print(threadName + ' is now crawling ' + page_url)  #Output to user what link is being crawled 
            print('Queued : ' + str(len(Spider.queue)) + ' | Crawled : ' + str(len(Spider.crawled)))    #Display the number of queued and crawled links
            Spider.addLinksToQueue(Spider.gatherLinks(page_url))    #Gather the URLs from the starting base_url and add it to the queue
            Spider.queue.remove(page_url)   #Remove the link which was crawled from the waiting list
            Spider.crawled.add(page_url)    #Add the link which is done being crawled
            Spider.update_queue_crawled()   #Converts both sets 'queue' and 'crawled' to file

    @staticmethod
    def gatherLinks(page_url):
        html_string = ' '
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':       #Checks if the response is of an HTML file and not any executable or PDF
                html_bytes = response.read()    #The response is the HTML which is in the form of bytes (1s and 0s)
                html_string = html_bytes.decode("utf-8")

            finder = linkFinder(Spider.base_url, page_url)      #Object of class linkFinder
            finder.feed(html_string)
        except:
            print('Error - Cannot crawl page')
            return set()
        return finder.pageLinks()

    @staticmethod
    def addLinksToQueue(links):     #Adds links gathered to the waiting list
        for url in links:
            if url in Spider.queue:         #If url is already present in the queue
                continue
            if url in Spider.crawled:       #If url is already crawled
                continue
            if url not in Spider.domain_url:    #The domain name must remain the same for all urls
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_queue_crawled():     #Converts the queue and crawled set to a file
        setToFile(Spider.queue, Spider.queueFile)
        setToFile(Spider.crawled, Spider.crawledFile)
