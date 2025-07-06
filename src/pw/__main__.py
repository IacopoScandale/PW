import json
import random
import string

from rich import print

from .data.strings import (
    AUTHOR,
    FILE_CHECK_PW,
    COMMANDS,
    FILE_COUNTER_JSON,
    DESCRIPTION,
    PW_COMM,
    PACKAGE_NAME,
    FILE_PW_OBJECTS_JSON,
)
from .data.utils import add_one_to_counter, ask_for_pw_two_times, encrypt_str


def init_setup() -> None:
    """
    Create the following files if they do not exist:

    - `pw_objects.json`
      - main file for storing data.

    - `usage_counter.json`
      - just for counting how many times each command is used

    - `check_pw.txt`
      - this file is used to see if input password is correct: if a
        password can decode this file than it is correct.

        **If this file exists then the package is already set up**

    If pw_objects does not exist the setup starts: it asks to create the
    main pw password which it will be used to encrypt all passwords.
    """

    if not FILE_CHECK_PW.exists():
        # create `pw/data/pw_objects.json` if it does not exists
        # (otherwise passwords could be lost)
        if not FILE_PW_OBJECTS_JSON.exists():
            # if it does not exist: create pw_objects.json as empty dict
            with open(FILE_PW_OBJECTS_JSON, "w") as jsonfile:
                json.dump(dict(), jsonfile)

        # enter PW main password and use it for first encryption
        print(
            "\nCreate your PW password:",
            "\n(this password will be asked everytime you use some",
            "encrypting / decrypting command)",
            "\n(DO NOT FORGET IT: it may not be changed if lost)\n",
        )
        pw: str = ask_for_pw_two_times()
        random_str: str = "".join(
            [random.choice(string.ascii_letters) for _ in range(10)]
        )
        encrypt_msg = encrypt_str(random_str, pw, check=False)

        # create `pw/data/check_pw.txt` file and write the encrypted message
        with open(FILE_CHECK_PW, "w") as txt:
            txt.write(encrypt_msg)

        print("\nSetup Completed!")


def show_infos() -> None:
    # start setup if it is required
    init_setup()

    # +1 to usage counter
    add_one_to_counter(PW_COMM)

    # load counter json as dict
    with open(FILE_COUNTER_JSON, "r") as jsonfile:
        usage_counter: dict[str, int] = json.load(jsonfile)

    # print title and all commands
    print(f"'{PACKAGE_NAME}' python package: '{DESCRIPTION}'")
    print(f"\n[bold]Commands:[/bold]{' ' * 14}[bold]Times Used:[/bold]")
    print("—" * 38)

    total: int = 0
    for i, command in enumerate(COMMANDS, 1):
        times_used: int = usage_counter.setdefault(command, 0)
        total += times_used
        print(f"{i:>4}. {command:<20} {times_used:>7}")

    print("—" * 38)
    print(f"      [bold]Total:[/bold]{' ' * 15}{total:>7}\n")
    print(f"[bold]Author:[/bold] '{AUTHOR}'")


if __name__ == "__main__":
    show_infos()
