from bs4 import BeautifulSoup
import urllib2

class FFXIAH( object ):
    
    def __init__( self ):
        self.__base_url = 'http://www.ffxiah.com/'
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

    