#the web root
# import whois
#
# print whois.whois('appspot.com')

#my first spider

#have a agent
#5xx retry
import re
import urllib2
import itertools
import urlparse
import robotparser
import Throttle

def download_network_page(url,user_agent='wswp', num_retries = 2):
    print 'Downloading : ', url
    headers = {'User-agent' : user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e :
        print 'Download error : ', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # rescursively retry 5xx http error
                return download_network_page(url, num_retries-1)
    return html

def crawl_sitemap(url):
    sitemap = download_network_page(url)
    links = re.findall('<loc>(.*?)<loc>', sitemap)
    for link in links:
        html = download_network_page(link)
        print html

def link_crawler(seed_url, link_regex):
    """
     crawlfrom the given seed URL following links matched by link_regex
     :param seed_url: 
     :param link_regex: 
     :return: 
     """
    #read the robots.txt
    rp = robotparser.RobotFileParser()
    rp.set_url('http://example.webscraping.com/robots.txt')
    rp.read()
    #set the agent's name
    user_agent = "667's Python Spider"
    #set the delay for crawl speed    5 second

    th = Throttle.Throttle(5)

    #set the crawl queue for crawled url
    crawl_queue = [seed_url]
    visited = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent,url):
            th.wait(url)
            html = download_network_page(url)
            print html
            # filter for links matching out regular expression
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)

                    if link not in visited:
                        visited.add(link)
                        crawl_queue.append(link)


def get_links(html):
    """
    return a list of links from html
    :param html: 
    :return: 
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)

    return webpage_regex.findall(html)

url = 'http://example.webscraping.com/sitemap.xml'
# url1 = 'http://httpstat.us/502'
# url2 = 'http://www.meetup.com/'
#
# crawl_sitemap(url)

#html = download_network_page(url2)
#print html
#
# for page in itertools.count(1):
#     url1 = 'http://example.webscraping.com/view/-%d' % page
#     html = download_network_page(url1)
#     if html is None:
#         break
#     else:
#         pass

# max_errors = 5
#
# num_errors = 0
#
# for page in itertools.count(1):
#     url1 = 'http://example.webscraping.com/view/-%d' % page
#     html = download_network_page(url1)
#     if html is None:
#         num_errors += 1
#         if num_errors == max_errors:
#             break
#     else:
#         num_errors = 0


url = 'http://example.webscraping.com'



link_crawler('http://example.webscraping.com', '/(index|view)')
