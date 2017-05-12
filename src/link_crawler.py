import download_network_page
import re
import urlparse

def link_crawler(seed_url, link_regex):
    """
     crawlfrom the given seed URL following links matched by link_regex
     :param seed_url: 
     :param link_regex: 
     :return: 
     """
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download_network_page(url)
        # filter for links matching out regular expression
        for link in get_links(html):
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link)
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

