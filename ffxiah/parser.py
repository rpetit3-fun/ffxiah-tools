from collections import OrderedDict
from bs4 import BeautifulSoup, Comment
import urllib2

class Parser(object):
    
    def __init__(self):
        self.__base_url = 'http://www.ffxiah.com'
        self.prices = []
        self.ffxi_servers()
        self.csv_order = ['name', 'sell01', 'buy01', 'price01', 'stock01',
                          'sell12', 'buy12', 'price12', 'stock12']
        self.items = OrderedDict()

    def __make_soup(self, url):
        request = urllib2.Request(url)
    
        # Change Server
        request.add_header('Cookie', 'sid=' + str(self.__sid))
        request.add_header('User-Agent',  
                           'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        html = urllib2.urlopen(request).read()
        html = html.replace('&#039;', '\'')
        return BeautifulSoup(html, "html.parser")
        
    def use_server(self, server):
        self.__sid = self.servers[server]
        
    def ffxi_servers(self):
        self.servers = {}
        self.inactive = []
        self.active = []
        
        request = urllib2.Request(self.__base_url)
        html = urllib2.urlopen(request).read()
        soup = BeautifulSoup(html, "lxml")
        
        # Inactive Servers
        for opts in soup.select('#ffxi-main-server-select optgroup option'):
            self.servers[str(opts.get_text())] = opts.get('value')
            self.inactive.append(str(opts.get_text()))
            
        # Active Servers
        for opts in soup.select('#ffxi-main-server-select option'):
            if not str(opts.get_text()) in self.servers:
                self.servers[str(opts.get_text())] = opts.get('value')
                self.active.append(str(opts.get_text()))
    
    def ah_items(self, fill_missing=False):
        self.__item_categories(fill_missing)
        
    def __item_categories(self, fill_missing):
        soup = self.__make_soup(self.__base_url + '/browse')
        for link in soup.select('ul li a[href]'):
            # Categories
            self.__item_prices(link.get('href'), fill_missing)
            
    def __item_prices(self, category_link, fill_missing):
        soup = self.__make_soup(self.__base_url + category_link)
        # Item Rows
        for row in soup.select('table tbody tr'):
            # Items Columns
            cols = row.findAll('td')
            
            # Some items didn't exist on retired servers, set price = 1 if so
            price = int(cols[4].get_text()) if cols[4].get_text() else 1
            if price == 0:
                price = 1
            
            # Item ID and Name
            id = str(cols[1].a.get('href')).split('item/')[1].split('/')[0]
            name = str(cols[1].get_text()).title().rstrip()
            stack = 1 if 'stack=1' in str(cols[1].a.get('href')) else 0

            if id not in self.items:
                # init a dict
                self.items[id] = {
                    'name': '',
                    'category': '',
                    'sell01': 1,
                    'buy01': 1,
                    'price01': None,
                    'stock01': 10,
                    'sell12': 0,
                    'buy12': 1,
                    'price12': None,
                    'stock12': 10
                }
            
            # Save Item info
            self.items[id]['category'] = category_link.split('/')[2]
            
            # Save Price
            if stack:
                name = name.replace('X12','').replace('X99','').rstrip()
                self.items[id]['name'] = name
                self.items[id]['sell12'] = 1
                
                if fill_missing and self.items[id]['price12'] == 1:
                    self.items[id]['price12'] = price
                elif not fill_missing:
                    if self.items[id]['price12'] and price > 1:
                        self.items[id]['price12'] = (price + self.items[id]['price12']) / 2
                    elif self.items[id]['price12'] is None:
                        self.items[id]['price12'] = price
            else:
                self.items[id]['name'] = name
                if fill_missing and self.items[id]['price01'] == 1:
                    self.items[id]['price01'] = price
                elif not fill_missing:
                    if self.items[id]['price01'] and price > 1:
                        self.items[id]['price01'] = (price + self.items[id]['price01']) / 2
                    elif self.items[id]['price01'] is None:
                        self.items[id]['price01'] = price
                