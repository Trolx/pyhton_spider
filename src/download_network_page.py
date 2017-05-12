import urllib2

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