from .data.utils import add_one_to_counter
from .data.strings import PW_COPY_SITE_PW
from .pw_class import copy_pw_from_json
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description="copies password linked to selected account to the clipboard"
  )
  parser.add_argument(
    "site_query", 
    help="substring of the site we are looking for e.g. 'hub' for 'github.com'"
  )
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  args: Namespace = get_arguments()

  copy_pw_from_json(args.site_query)

  add_one_to_counter(PW_COPY_SITE_PW)