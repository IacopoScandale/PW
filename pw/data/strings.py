import os

# strings
PACKAGE_NAME = "pw"
MAIN_COMM_NAME = "pw"
AUTHOR = "Iacopo Scandale"
LICENSE = "GNU"
VERSION = "2.0"
DESCRIPTION = (
  "CLI Password Manager.\n"
  f"Type '{MAIN_COMM_NAME}' for some infos,\n"
  f"Type '{MAIN_COMM_NAME} -h' for other infos"
)


# commands
COMMANDS: list[str] = [
  PW_ADD_COMM_NAME := "add",
  PW_INFO_COMM_NAME := "info",
  PW_ALL_INFO_COMM_NAME := "all_info",
  PW_COPY_COMM_NAME := "copy",
  PW_LIST_COMM_NAME := "list",
  PW_EDIT_COMM_NAME := "edit",
  PW_REMOVE_COMM_NAME := "remove",
]

# command help messages
PW_ADD_HELP = "Add a site account to the database."
PW_INFO_HELP = "Show some infos linked to chosen site found from site query"
PW_ALL_INFO_HELP = (
  "Prints all infos linked to chosen site found from site query "
  "requires PW password"
)
PW_COPY_HELP = (
  "Copy the password associated with the selected account to the clipboard"
)
PW_LIST_HELP = (
  "List all sites in the database. Also a query can be passed to filter the list"
)
PW_EDIT_HELP = "Find an account from a site query and edit infos"
PW_REMOVE_HELP = "Find an account from a site query and remove it"


DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))
"""
Full path `pw/data` folder
"""

INFO_FOLDER = f"{PACKAGE_NAME}.egg-info"
"""
Egg info folder name
"""

COUNTER_JSON = os.path.join(DATA_FOLDER, "usage_counter.json")
"""
Full path `pw/data/usage_counter.json`
"""
PW_OBJECTS = os.path.join(DATA_FOLDER, "pw_objects.json")
"""
Full path of the file `pw/data/pw_objects.json`
"""
PW_CSV = os.path.join(DATA_FOLDER, "pw.csv")
"""
Full path of file `pw/data/pw.csv`
"""
CHECK_PW = os.path.join(DATA_FOLDER, "check_pw.txt")
"""
Full path of the .txt file containing an encrypted string. 

Use it to check if password is correct: if used password cannot 
decode this string then it is wrong. This is useful when we add
new passwords. 
"""