#!/usr/bin/env python
import argparse
import keyring
import getpass
import sys
from tabulate import tabulate
from whos_on_location import WhosOnLocation

try:
    input = raw_input
except NameError:
    input = input

EMAIL_KEY = 'whosonlocation.email'
PASS_KEY = 'whosonlocation.pass'


def set_credentials():
    email = input('Enter email\n> ')
    password = input('Enter password\n> ')
    password_verify = input('Verify password\n> ')
    if password != password_verify:
        print("Passwords don't match!")
    else:
        user = getpass.getuser()
        keyring.set_password(EMAIL_KEY, user, email)
        keyring.set_password(PASS_KEY, user, password)
        print("Credentials set!")


def init_location():
    user = getpass.getuser()
    email = keyring.get_password(EMAIL_KEY, user)
    password = keyring.get_password(PASS_KEY, user)
    if not email or not password:
        print("You need to set credentials!")
        sys.exit(1)

    return WhosOnLocation(email, password)


def set_status(location, status):
    if status == 'onsite':
        location.on_site()
    elif status == 'offsite':
        location.off_site()
    print("Your status is: %s" % location.get_status())


def search(location, search_term):
    results = location.search(search_term)
    if results:
        print(tabulate(results, headers='keys'))


parser = argparse.ArgumentParser(description='Set your status for WhosOnLocation.com')
arg_group = parser.add_mutually_exclusive_group()
arg_group.add_argument('--set-status',
                       metavar='STATUS',
                       type=str,
                       choices=('onsite', 'offsite'),
                       dest='status',
                       help='Set the status. Allowed values (onsite, offsite)')

arg_group.add_argument('--set-creds',
                       action='store_true',
                       help='Set email/password for whosonlocation.com')
arg_group.add_argument('--search',
                       metavar='QUERY',
                       type=str,
                       help='Search term')

args = parser.parse_args()

location = init_location()
if not location.login():
    print('Login failed')
else:
    if args.set_creds:
        set_credentials()
    elif args.status:
        set_status(location, args.status)
    elif args.search:
        search(location, args.search)
    else:
        print("WTF")

