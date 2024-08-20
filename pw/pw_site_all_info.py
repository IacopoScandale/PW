from .data.utils import add_one_to_counter
from .data.strings import PW_ALL_INFO_COMM_NAME
from .pw_class import print_site_info_command
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description=(
      "prints all infos linked to chosen site found from site query "
      "(requires PW password)"
    )
  ) 
  parser.add_argument(
    "site_query", 
    help="substring of the site we are looking for e.g. 'hub' for 'github.com'"
  )
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  args: Namespace = get_arguments()
  
  print_site_info_command(args.site_query, True)

  add_one_to_counter(PW_ALL_INFO_COMM_NAME)