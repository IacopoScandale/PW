help_message = """
Add pw Command:

Adds an account to the database.

If no arguments given starts guided input asking

Usage:
1. pw.add
2. pw.add <site> <username> <email> <site password> <other 1> <other 2> ...
"""

from pw_class import PW
from Data.constants import help_and_error
import os, sys


help_and_error(help_message, sys.argv)

# change directory to main project directory
os.chdir(os.path.dirname(sys.argv[0]))

# case
if len(sys.argv) == 1:
    # ask manually for account info
    site = input("Enter site: ")
    username = input("Username: ")
    email = input("Email: ")
    pw = input("Enter site pw: ")
    other = []
    print("Enter other options (--exit to stop): ")
    while True:
        info = input(" · ")
        if info == "--exit":
            break
        other.append(info)

# at least site, username, email, site_password
elif len(sys.argv) >= 5:
    site, username, email, pw = sys.argv[1:5]
    if len(sys.argv) > 5:
        other = sys.argv[5:]
    else:
        other = []

# wrong arg number
else:
    print(f"ERROR: Wrong Argument Number")
    print("type 'command_name --help' for more info")
    sys.exit()


# create obj and add to database
pw_obj = PW(site, username, email, pw, other, encrypted=False)
pw_obj.add_to_database()

# show some data
print(pw_obj.print_site())