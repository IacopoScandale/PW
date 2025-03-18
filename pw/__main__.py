from .data.utils import add_one_to_counter, encrypt_str, ask_for_pw_two_times
from .data.strings import *
import os
import json
import random
import string


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

  if not os.path.exists(CHECK_PW):

    # create usage_counter.json file
    if not os.path.exists(COUNTER_JSON):
      with open(COUNTER_JSON, "w") as jsonfile:
        json.dump(dict(), jsonfile)

    # create `pw/data/pw_objects.json` if it does not exists 
    # (otherwise passwords could be lost)
    if not os.path.exists(PW_OBJECTS):
      # if it does not exist: create pw_objects.json as empty dictionary
      with open(PW_OBJECTS, "w") as jsonfile:
        json.dump(dict(), jsonfile)

    # enter PW main password and use it for first encription
    print(
      "\nCreate your PW password:",
      "\n(this password will be asked everytime you use some encrypting /",
      "decrypting command)",
      "\n(DO NOT FORGET IT: it may not be changed if lost)\n",
    )
    pw: str = ask_for_pw_two_times()
    random_str: str = "".join([random.choice(string.ascii_letters) for _ in range(10)])
    encrypt_msg = encrypt_str(random_str, pw, check=False)

    # create `pw/data/check_pw.txt` file and write the encrypted message
    with open(CHECK_PW, "w") as txtfile:
      txtfile.write(encrypt_msg)

    print(f"\nSetup Completed!")


def show_infos() -> None:
  here: str = os.path.dirname(os.path.abspath(__file__)) 
  full_path_counter_json: str = os.path.join(here, COUNTER_JSON)

  # start setup if it is required
  init_setup()

  # +1 to usage counter
  add_one_to_counter(MAIN_COMM_NAME)

  # open counter json as dictionary
  with open(full_path_counter_json, "r") as jsonfile:
    usage_counter: dict[str,int] = json.load(jsonfile)

  # print title and all commands
  print(f"Package '{PACKAGE_NAME}'")
  print(f"Description: {DESCRIPTION}")
  print(f"\n\ncommands:{' '*15}times used:")
  print("—"*38)

  total: int = 0
  for i, command in enumerate(COMMANDS, 1):
    times_used: int = usage_counter.setdefault(command, 0)
    total += times_used
    print(f"{i:>4}. {command:<20} {times_used:>7}")

  print("—"*38)
  print(f"      Total:{' '*15}{total:>7}\n")


if __name__ == "__main__":
  show_infos()