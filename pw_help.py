help_message = """
Usage: pw

Output: displays all pw commands
"""

from data_tmp.utils import help_and_error
from data_tmp.strings import PW_ADD_COMM_NAME, PW_COPY_SITE_PW, PW_HELP, PW_INFO_COMM_NAME, PW_ALL_INFO_COMM_NAME
import sys




help_and_error(help_message, sys.argv, 0)

# list of command names
command_names = [PW_HELP, PW_ADD_COMM_NAME, PW_COPY_SITE_PW, PW_INFO_COMM_NAME, PW_ALL_INFO_COMM_NAME]

print("\n--- PW COMMANDS ---", end="\n\n")
for i, cmd in enumerate(command_names):
  print(f" {i+1}.\t{cmd}")

print("\n (type '`command_name` -h' for more info)")