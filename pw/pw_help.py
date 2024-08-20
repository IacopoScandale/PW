from .data.utils import add_one_to_counter
from .data.strings import PACKAGE_NAME, COUNTER_JSON, COMMANDS
from argparse import ArgumentParser, Namespace
import os
import json


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description="Shows all PW commands"
  )
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  _ = get_arguments()

  here: str = os.path.dirname(os.path.abspath(__file__)) 
  full_path_counter_json: str = os.path.join(here, COUNTER_JSON)

  # +1 to usage counter
  add_one_to_counter(PACKAGE_NAME)

  # open counter json as dictionary
  with open(full_path_counter_json, "r") as jsonfile:
    usage_counter: dict[str,int] = json.load(jsonfile)

  # print title and all commands
  print(f"pw package\n\ncommands:{' '*15}times used:")

  for i, command in enumerate(COMMANDS.keys(), 1):
    times_used: int = usage_counter.setdefault(command, 0)
    print(f"{i:>4}. {command:<20} {times_used:>7}")

  print("\nType 'command_name -h' for more info")