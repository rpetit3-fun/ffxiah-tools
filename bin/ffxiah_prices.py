#! /usr/bin/python
'''
    ffxi_scraper.py
    
    For each auctionable item in FFXI scrape the median price from FFXIAH.com.
'''
import argparse as ap
from ffxiah.parser import Parser

if __name__ == '__main__':
    ffxiah = Parser()
    
    parser = ap.ArgumentParser(prog='ffxiah_scraper.py', 
                               conflict_handler='resolve', 
                               description="Scrape prices from ffxiah.com")

    parser.add_argument('-s', '--server', 
        default='Carbuncle',
        choices = ffxiah.servers.keys(),
        help=('Server to scrape from.(ACTIVE: {0} || INACTIVE: {1})'.format(
            ', '.join(ffxiah.active),
            ', '.join(ffxiah.inactive)
        )),
        metavar=''
    )
    parser.add_argument('-h', '--help', action='help', 
                        help='Show this help message and exit')
    
    args = parser.parse_args()
    
    # Set Server Prices to scrape
    ffxiah.use_server(args.server)
    
    # Get prices
    ffxiah.ah_items()
    
    # Print Prices
    for item in ffxiah.prices:
        print '{0}\t{1}\t{2}'.format(
            item['id'],
            item['stack'],
            item['price']
        )
    