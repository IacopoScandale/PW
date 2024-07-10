import os, json
from Data.constants import PW_OBJECTS, CONFIG_JSON, CHECK_PW, COMMANDS_BAT, COMMANDS_SH, encrypt_str
from Data.constants import PW_ADD_COMM_NAME, PW_INFO_COMM_NAME, PW_ALL_INFO_COMM_NAME, PW_COPY_SITE_PW
from getpass import getpass
"""
PW Setup:

Windows: double click on setup.py or call from terminal
Linux: call this file from terminal
"""

# title
print("=================================")
print("||          PW SETUP           ||")
print("=================================",end="\n\n")


# install location
print("· Check if folder PW is in following path, otherwise insert it manually or call this file from terminal\n")
ans_loc = input(f"Installing PW in current location: {os.getcwd()}?\n [y,n]: ")
if ans_loc in "yYsS":
  pass
elif ans_loc in "nN":
  ans_loc = input("Insert location or restart installing from location:\n ")
  os.chdir(ans_loc)
else:
  raise ValueError("answer must be 'y' or 'n'")


# create `Data/pw_objects.json` if it does not exists (otherwise passwords could be lost)
if not os.path.exists(PW_OBJECTS):
  # if it does not exist: create pw_objects.json as empty dictionary
  with open(PW_OBJECTS, "w") as jsonfile:
    json.dump(dict(), jsonfile)
else:
  raise OSError("Cannot delete 'pw_objects.json' file: it could contain some important data.\nMove or delete it and restart setup.py")


# write path in `Data/config.json` dict
config = dict()
config["main folder path"] = os.getcwd()
# save json config file
with open(CONFIG_JSON, "w") as jsonfile:
  json.dump(config, jsonfile, indent=2)


# install cryptography (TODO try in an environment)
print("Installing from file requirements.txt")
os.system("pip install -r requirements.txt")


# ask for PW password
print("\nCreate your PW password:")
print("(this password will be asked every time you use some encrypting / decrypting command)")
print("(DO NOT FORGET IT: it may not be changed if lost)")
# enter pw 2 times
pw = getpass("Create PW password: ")
pw_check = getpass("Confirm PW password: ")
if pw != pw_check:
  raise ValueError("Passwords do not match")
# encrypt word main path message using pw
encrypt_msg = encrypt_str(config["main folder path"], pw, check=False)
# create `check_pw.txt file`
with open(CHECK_PW, "w") as txtfile:
  # write some encrypted text
  txtfile.write(encrypt_msg)


def windows_alias_command_line(command_name:str, filename_py:str, args:str="") -> str:
  """
  Create windows command line for file comands.bat
  Input:
  - `filename_py:str` name of the python file to call
  - `command_name:str` name of the alias
  - `args:str=""` insert other default arguments (separated by a space) if needed
  """
  command_file_path = os.path.join(os.getcwd(), filename_py)
  return f"doskey {command_name} = python {command_file_path} {args} $*\n"

# TODO create .bat and .sh aliases files
if os.name == "nt":
  # windows echo off
  commands = "@echo off\n\n"
  # pw.add command
  commands += windows_alias_command_line(PW_ADD_COMM_NAME, "pw_add.py")
  # pw.info command
  commands += windows_alias_command_line(PW_INFO_COMM_NAME, "pw_site_info.py", args="False")
  # pw.all_info command
  commands += windows_alias_command_line(PW_ALL_INFO_COMM_NAME, "pw_site_info.py", args="True")
  # copy pw to clipboard
  commands += windows_alias_command_line(PW_COPY_SITE_PW, "pw_copy.py")


  # TODO add more commands


  
  # Write commands on commands.bat file
  with open(COMMANDS_BAT, "w") as txtfile:
    txtfile.write(commands)



  # TODO add automatically file to regedit...


elif os.name == "posix":
  # TODO
  pass





  # TODO add automatically file to current shell.rc

else:
  raise OSError(f"Your os {os.name} is not supported")


os.system("pause")