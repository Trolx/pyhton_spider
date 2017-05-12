import re
import download_network_page

def crawl_sitemap(url):
    sitemap = download_network_page(url)
    links = re.findall('<loc>(.*?)<loc>', sitemap)
    for link in links:
        html = download_network_page(link)
        print html