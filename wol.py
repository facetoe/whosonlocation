#!/usr/bin/env python
import argparse
import keyring
import getpass
import sys
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


def set_status(status):
    user = getpass.getuser()
    email = keyring.get_password(EMAIL_KEY, user)
    password = keyring.get_password(PASS_KEY, user)
    if not email or not password:
        print("You need to set credentials!")
        return

    location = WhosOnLocation(email, password)
    if location.login():
        if status == 'onsite':
            location.on_site()
        elif status == 'offsite':
            location.off_site()

        print("Your status is: %s" % location.get_status())
    else:
        print("Login Failed")


parser = argparse.ArgumentParser(description='Set your status for WhosOnLocation.com')
parser.add_argument('--set-status', metavar='STATUS', type=str, choices=('onsite', 'offsite'),
                    help='Set the status. Allowed values (onsite, offsite)')
parser.add_argument('--set-creds', action='store_true',
                    help='Set email/password for whosonlocation.com')

args = parser.parse_args()
if args.set_status and args.set_creds:
    print("--set-status and --set-creds are mutually exclusive")
    sys.exit(1)
elif not args.set_creds and not args.set_status:
    print("--set-status or --set-creds are required")
    sys.exit(1)

if args.set_creds:
    set_credentials()
elif args.set_status:
    set_status(args.set_status)
else:
    print("WTF")
