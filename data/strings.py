import os

PIP_VENV_WIN = "venv\\Scripts\\pip3.exe"
PIP_VENV_LINUX = ""

PYTHON_VENV_WIN = "venv\\Scripts\\python.exe"
PYTHON_VENV_LINUX = ""

DATA_FOLDER_NAME = "data"
"""
Name of the folder containg config files etc
"""

PW_OBJECTS = os.path.join(DATA_FOLDER_NAME, "pw_objects.json")
"""
Relative path of file `pw_objects.json`
"""

PW_CSV = os.path.join(DATA_FOLDER_NAME, "pw.csv")
"""
Relative path of file `pw.csv`
"""

OLD_PW_OBJECTS = os.path.join(DATA_FOLDER_NAME, "OLD_pw_objects.json")
"""
Relative path of file `pw_objects.json` when renamed by `uninstall.py`
"""

CHECK_PW = os.path.join(DATA_FOLDER_NAME, "check_pw.txt")
"""
Relative path txt file containing an encrypted string. 

Use it to check if password is correct: if used password cannot 
decode this string then it is wrong. This is useful when we add
new passwords. 
"""

CONFIG_JSON = os.path.join(DATA_FOLDER_NAME, "config.json")
"""
Relative path to `config.json` file
"""

COMMANDS_BAT = os.path.join(DATA_FOLDER_NAME, "commands.bat")
"""
Relative path to commands.bat file containing command aliases
"""

COMMANDS_SH = os.path.join(DATA_FOLDER_NAME, "commands.sh")
"""
Relative path to commands.sh file containing command aliases
"""

# alias names
PW_ADD_COMM_NAME = "pw_.add"
"""
Alias name calling `pw_add.py`
"""

PW_INFO_COMM_NAME = "pw_.info"
"""
Alias name calling `pw_site_info.py False`
"""

PW_ALL_INFO_COMM_NAME = "pw_.all_info"
"""
Alias name calling `pw_site_info.py True`
"""

PW_COPY_SITE_PW = "pw_.copy"
"""
Alias name calling `pw_copy.py`
"""

PW_HELP = "pw_"
"""
Alias name calling `pw_help.py`
"""