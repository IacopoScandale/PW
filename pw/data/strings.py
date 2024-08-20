import os


PACKAGE_NAME: str = "pw"
DATA_FOLDER: str = os.path.dirname(os.path.abspath(__file__))
"""
Full path `pw/data` folder
"""
COMMANDS_COPY_FOLDER: str = "Commands"
"""
Commands folder name
"""
INFO_FOLDER: str = f"{PACKAGE_NAME}.egg-info"
"""
Egg info folder name
"""
VENV_FOLDER: str = "venv"
"""
venv folder name
"""

VENV_SCRIPTS_FOLDER_WIN: str = os.path.join(VENV_FOLDER, "Scripts")
VENV_SCRIPTS_FOLDER_LINUX: str = os.path.join(VENV_FOLDER, "bin")

COUNTER_JSON: str = os.path.join(DATA_FOLDER, "usage_counter.json")
"""
Full path `pw/data/usage_counter.json`
"""
PW_OBJECTS: str = os.path.join(DATA_FOLDER, "pw_objects.json")
"""
Full path of the file `pw/data/pw_objects.json`
"""
PW_CSV: str = os.path.join(DATA_FOLDER, "pw.csv")
"""
Full path of file `pw/data/pw.csv`
"""
CHECK_PW: str = os.path.join(DATA_FOLDER, "check_pw.txt")
"""
Full path of the .txt file containing an encrypted string. 

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