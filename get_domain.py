from urllib.parse import urlparse

def get_subdomain_name(url):
    try:
        return urlparse(url).netloc     #Returns the sub-domain. Ex: 'mail.google.com'
    except:
        return ''                       #Return NULL 

def get_domain_name(url):   #Converts 'mail.google.com' to 'google.com'
    try:
        sub_domain = get_subdomain_name(url).split('.')
        return sub_domain[-2] + '.' + sub_domain[-1]
    except:
        return ''
        


