#! /usr/bin/python

import argparse as ap
import ffxiah


"""
    ffxi_scraper.py
    
    For each auctionable item in FFXI scrape the median price from FFXIAH.com.
    
"""



if __name__ == '__main__':
    ffxiah = ffxiah.FFXIAH()

    parser = ap.ArgumentParser(prog='ffxiah_scraper.py', 
                               conflict_handler='resolve', 
                               description="Scrape prices from ffxiah.com")

    parser.add_argument('-s', '--server', default='Carbuncle',
                        choices = ffxiah.servers.keys(),
                        help='Server to scrape prices from. ( ACTIVE: ' + 
                             ', '.join( ffxiah.active ) + ' | INACTIVE: ' +
                             ', '.join( ffxiah.inactive ) + ')',
                        metavar='')
    parser.add_argument('-h', '--help', action='help', 
                        help='Show this help message and exit')
    
    args = parser.parse_args()
    
    # Set Server Prices to scrape
    ffxiah.use_server( args.server )
    
    # Get prices
    ffxiah.get_prices()

    