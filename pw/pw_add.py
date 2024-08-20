from .data.utils import add_one_to_counter
from .data.strings import PW_ADD_COMM_NAME
from .pw_class import PW
from argparse import ArgumentParser, Namespace
import os
import sys


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description="Adds a site account to the database."
  )
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  # change directory otherwise it won't find pw_objects.json
  os.chdir(os.path.dirname(os.path.abspath(__file__)))

  _ = get_arguments()

  # ask manually for account info
  try:
    site: str = input(f'{"Enter site: ":>17}')
    username: str = input(f'{"Username: ":>17}')
    email: str = input(f'{"Email: ":>17}')
    pw: str = input(f'{"Site password: ":>17}')
  except KeyboardInterrupt:
    sys.exit()

  other: list[str] = []
  print("  \nEnter other private infos:")
  print("  (leave blank to stop)")

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
  pw_obj = PW(site, username, email, pw, other, encrypted=False)
  pw_obj.add_to_database()

  # show some data
  print(pw_obj.print_site())

  add_one_to_counter(PW_ADD_COMM_NAME)