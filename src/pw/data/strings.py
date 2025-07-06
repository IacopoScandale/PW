from pathlib import Path


# strings
PACKAGE_NAME: str = "pw"
DESCRIPTION: str = "CLI Password Manager."
AUTHOR: str = "Iacopo Scandale"


# commands
COMMANDS: list[str] = [
    PW_COMM := "pw",
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
    "Prints all infos linked to chosen site found from site query requires PW password"
)
PW_COPY_HELP = "Copy the password associated with the selected account to the clipboard"
PW_LIST_HELP = (
    "List all sites in the database. Also a query can be passed to filter the list"
)
PW_EDIT_HELP = "Find an account from a site query and edit infos"
PW_REMOVE_HELP = "Find an account from a site query and remove it"


# paths
DIR_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
DIR_SCRIPTS: Path = DIR_ROOT / "src" / "pw"
DIR_DATA: Path = DIR_SCRIPTS / "data"

FILE_COUNTER_JSON: Path = DIR_DATA / "usage_counter.json"
"""
Full path of the .json file containing the number of times each command
was used
"""
if not FILE_COUNTER_JSON.exists():
    FILE_COUNTER_JSON.write_text("{}")

FILE_PW_OBJECTS_JSON = DIR_DATA / "pw_objects.json"
"""
Full path of the .json file containing encrypted infos
"""
FILE_PW_CSV = DIR_DATA / "pw.csv"
"""
Full path of the .csv file containing the plain text passwords ready to 
be exported
"""
FILE_CHECK_PW = DIR_DATA / "check_pw.txt"
"""
Full path of the .txt file containing an encrypted string. 

Use it to check if password is correct: if used password cannot 
decode this string then it is wrong. This is useful when we add
new passwords. 
"""
