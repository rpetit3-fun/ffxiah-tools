#! /usr/bin/python
'''
ffxiah_prices.py

For each auctionable item in FFXI scrape the median price from FFXIAH.com.
'''
import argparse as ap
from ffxiah.parser import Parser
from ffxiah.dspdb import DSPDB

if __name__ == '__main__':
    ffxiah = Parser()

    parser = ap.ArgumentParser(prog='ffxiah_prices.py',
                               conflict_handler='resolve',
                               description="Scrape prices from ffxiah.com")

    parser.add_argument(
        '-s', '--server',
        default='Carbuncle',
        help=('Server to scrape from.(ACTIVE: {0} || INACTIVE: {1})'.format(
            ', '.join(ffxiah.active),
            ', '.join(ffxiah.inactive)
        )),
        metavar=''
    )
    parser.add_argument('-m', '--missing',
        default='Carbuncle',
        help=('Server to scrape  missing prices from.(ACTIVE: {0})'.format(
            ', '.join(ffxiah.active)
        )),
        metavar=''
    )
    parser.add_argument('-h', '--help', action='help',
                        help='Show this help message and exit')

    args = parser.parse_args()

    for server in args.server.split(','):
        # Set Server Prices to scrape
        ffxiah.use_server(server)

        # Get prices
        ffxiah.ah_items()

    # fill missing prices with an active server
    ffxiah.use_server(args.missing)
    ffxiah.ah_items(fill_missing=True)

    # Print Prices
    print 'itemid,{0}'.format(",".join(ffxiah.csv_order))
    for itemid in ffxiah.items:
        d = ffxiah.items[itemid]

        print ','.join(str(a) for a in [
            itemid,
            d['name'],
            d['sell01'],
            d['buy01'],
            d['price01'],
            d['stock01'],
            d['sell12'],
            d['buy12'],
            d['price12'],
            d['stock12']
        ])
