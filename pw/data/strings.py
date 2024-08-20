import os

PACKAGE_NAME: str = "pw"
COMMANDS_COPY_FOLDER: str = "Commands"
DATA_FOLDER: str = "data"
INFO_FOLDER: str = f"{PACKAGE_NAME}.egg-info"
VENV_FOLDER: str = "venv"

VENV_SCRIPTS_FOLDER_WIN: str = os.path.join(VENV_FOLDER, "Scripts")
VENV_SCRIPTS_FOLDER_LINUX: str = os.path.join(VENV_FOLDER, "bin")

COUNTER_JSON_NAME: str = "usage_counter.json"
COUNTER_JSON: str = os.path.join(DATA_FOLDER, COUNTER_JSON_NAME)



PW_OBJECTS: str = os.path.join(DATA_FOLDER, "pw_objects.json")
"""
Relative path of file `pw_objects.json`
"""


PW_CSV: str = os.path.join(DATA_FOLDER, "pw.csv")
"""
Relative path of file `pw.csv`
"""

OLD_PW_OBJECTS: str = os.path.join(DATA_FOLDER, "OLD_pw_objects.json")
"""
Relative path of file `pw_objects.json` when renamed by `uninstall.py`
"""

CHECK_PW: str = os.path.join(DATA_FOLDER, "check_pw.txt")
"""
Relative path txt file containing an encrypted string. 

Use it to check if password is correct: if used password cannot 
decode this string then it is wrong. This is useful when we add
new passwords. 
"""



# commands
PW_ADD_COMM_NAME: str = "pw.add"
PW_INFO_COMM_NAME: str = "pw.info"
PW_ALL_INFO_COMM_NAME: str = "pw.all_info"
PW_COPY_SITE_PW: str = "pw.copy"


COMMANDS: dict[str,str] = {
  PACKAGE_NAME: "pw_help",
  PW_ADD_COMM_NAME: "pw_add",
  PW_INFO_COMM_NAME: "pw_site_info",
  PW_ALL_INFO_COMM_NAME: "pw_site_all_info",
  PW_COPY_SITE_PW: "pw_copy",
}