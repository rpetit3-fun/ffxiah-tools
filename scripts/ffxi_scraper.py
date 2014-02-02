#! /usr/bin/python

import argparse
from bs4 import BeautifulSoup
import urllib2

"""
    ffxi_scraper.py
    
    For each auctionable item in FFXI scrape the median price from FFXIAH.com.
    
"""

if __name__ == '__main__':   
    parser = argparse.ArgumentParser(prog='ffxiah_scraper.py', 
                                     conflict_handler='resolve', 
                                     description="Scrape prices from ffxiah.com")

    parser.add_argument('-s', '--server', default='Carbuncle',
                        help='Server to scrape prices from. (default: %(default)s)', 
                        metavar="STRING")
    parser.add_argument('-h', '--help', action='help', 
                        help='Show this help message and exit')
    
    args = parser.parse_args()

    
    
    url = 'http://www.ffxiah.com/browse'
    request = urllib2.Request(url)

    # Change Server
    request.add_header('Cookie', 'sid=8')
    request.add_header('User-Agent',  'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    html = urllib2.urlopen(request).read()
    
    soup = BeautifulSoup(html, "lxml")
    for link in soup.select('ul ul li a[href]'):
        # Categories
        print link.get('href')    
    
