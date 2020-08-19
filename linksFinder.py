from html.parser import HTMLParser
from urllib import parse

class linkFinder (HTMLParser):   #Use HTMLParser for this class

    #Constructor
    def __init__(self, base_url, page_url):
        super().__init__()          #Super class initialization 
        self.base_url = base_url    #For the main URL (homepage URL)
        self.page_url = page_url    #For the URLs of different pages on the homepage
        self.links = set()          #Store links in the set

    def error (self, message):   #To catch errors
        pass

    #Example
    #< a href = "/contests/1043,1069">Codeforces Round #519</a>
    #Here, the value is "/contests/1043,1069". The base url for this example is 'http://codeforces.com'
    #We need to join this base url with the value otherwise it causes problems while scraping
    def handle_startTag (self, tag, attributes):
        if tag == 'a':   #Stands for 'anchor' which has the URL
            for  (attribute, value) in attributes:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)   #Joins the base url with the value
                    self.links.add(url)     #Add this url to the links set

    #Returns the links on that page
    def pageLinks (self):
        return self.links                
