#! /usr/bin/env python
'''
    update_categories.py
    
    Compare FFXIAH item categories to DSP categories. Update any items with 
    an incorrect category id.
'''
import argparse as ap
from ffxiah.parser import Parser
from ffxiah.dspdb import DSPDB

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='update_categories.py', 
                               conflict_handler='resolve', 
                               description="Compare category IDs")

    parser.add_argument('-h', '--help', action='help', 
                        help='Show this help message and exit')
    
    args = parser.parse_args()
    
    # Set Server to scrape
    ffxiah = Parser()
    ffxiah.use_server('Carbuncle')
    
    # Get FFXIAH item info
    ffxiah.ah_items()
    
    # Get DSP item info
    dspdb = DSPDB()
    dspdb.dsp_items()
    
    # Compare categories
    for item_id in ffxiah.items:
        if ffxiah.items[item_id]['category'] != dspdb.items[item_id]['category']:
            dspdb.update_category(item_id, ffxiah.items[item_id]['category'])
            print 'Updated Category For {0} ({1}, {2}->{3})'.format(
                ffxiah.items[item_id]['name'], 
                item_id, 
                ffxiah.items[item_id]['category'],
                dspdb.items[item_id]['category']
            )
