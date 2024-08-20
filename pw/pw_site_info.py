from .data.utils import add_one_to_counter
from .data.strings import PW_INFO_COMM_NAME
from .pw_class import print_site_info_command
from argparse import ArgumentParser, Namespace
import os


def get_arguments() -> Namespace:
  parser: ArgumentParser = ArgumentParser(
    description="prints some infos linked to chosen site found from site query"
  ) 
  parser.add_argument(
    "site_query", 
    help="substring of the site we are looking for e.g. 'hub' for 'github.com'"
  )
  args: Namespace = parser.parse_args()
  return args


def main() -> None:
  # change directory otherwise it won't find pw_objects.json
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  
  args: Namespace = get_arguments()
  

  print_site_info_command(args.site_query, False)

  add_one_to_counter(PW_INFO_COMM_NAME)