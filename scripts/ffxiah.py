from bs4 import BeautifulSoup, Comment
import urllib2

class FFXIAH( object ):
    
    def __init__( self ):
        self.__base_url = 'http://www.ffxiah.com'
        self.__categories = []
        self.__items = []
        self.get_servers()
        
    def get_servers( self ):
        self.servers = {}
        self.inactive = []
        self.active = []
        
        request = urllib2.Request( self.__base_url )
        html = urllib2.urlopen( request ).read()
        soup = BeautifulSoup( html, "lxml" )
        
        # Inactive Servers
        for opts in soup.select('#ffxi-main-server-select optgroup option'):
            self.servers[ str(opts.get_text()) ] = opts.get('value')
            self.inactive.append( str(opts.get_text()) )
            
        # Active Servers
        for opts in soup.select('#ffxi-main-server-select option'):
            if not str(opts.get_text()) in self.servers:
                self.servers[ str(opts.get_text()) ] = opts.get('value')
                self.active.append( str(opts.get_text()) )
                
    def use_server( self, server ):
        self.__sid = self.servers[ server ]
        
    def __make_soup( self, url ):
        request = urllib2.Request(url)
    
        # Change Server
        request.add_header('Cookie', 'sid=' + str(self.__sid))
        request.add_header('User-Agent',  
                           'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        html = urllib2.urlopen(request).read()
        html = html.replace('&#039;', '\'')
        
        return BeautifulSoup(html, "html.parser")
        
    def get_prices( self ):
        self.__get_categories()
            
    def __get_categories( self ):
        soup = self.__make_soup( self.__base_url + '/browse' )

        for link in soup.select('ul ul li a[href]'):
            # Categories
            self.__get_items( link.get('href') )
            
    def __get_items( self, category ):
        soup = self.__make_soup( self.__base_url + category )
        # Item Rows
        for row in soup.select('table tbody tr'):
            # Items Columns
            cols = row.findAll('td')
            
            # Some items didn't exist on retired servers, set price = 0 if so
            price = cols[4].get_text() if cols[4].get_text() else 0
            
            # Item ID and Name
            id = str(cols[1].a.get('href')).split('item/')[1].split('/')[0]
            name = str(cols[1].get_text()).title()
            stack = 1 if 'stack=1' in str(cols[1].a.get('href')) else 0
            print id, '\t', name, '\t', price, '\t', stack
            