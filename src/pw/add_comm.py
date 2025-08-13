"""
Add a new site into the database
"""

import sys

from rich import print

from pw.data.strings import PW_ADD_COMM_NAME
from pw.data.utils import add_one_to_counter, get_edit_date
from pw.pw_class import PW


def add_comm() -> None:
    """
    Add a password to the database
    """
    # ask manually for account info
    try:
        site: str = input(f"{'Enter site: ':>17}")
        username: str = input(f"{'Username: ':>17}")
        email: str = input(f"{'Email: ':>17}")
        pw: str = input(f"{'Site password: ':>17}")
    except KeyboardInterrupt:
        sys.exit()

    other: list[str] = []
    print("  \nEnter other private infos:")
    print("  [bright_black](leave blank to stop)[/bright_black]")

    while True:
        try:
            info: str = input("   · ")
            if info.strip() == "":
                break
            else:
                other.append(info.strip())
        except KeyboardInterrupt:
            sys.exit()

    # create obj and add to database
    pw_obj = PW(
        site, username, email, pw, other, encrypted=False, edit_date=get_edit_date()
    )
    pw_obj.add_to_database()

    # show some data
    print(pw_obj.print_site())

    # +1 to usage counter
    add_one_to_counter(PW_ADD_COMM_NAME)


if __name__ == "__main__":
    add_comm()
