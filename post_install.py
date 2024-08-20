from pw.data.utils import encrypt_str
from pw.data.strings import *
from getpass import getpass
import subprocess
import os
import sys
import json


def print_path(path: str) -> None:
  paths: list[str] = path.split(os.pathsep)
  for path in paths:
    print(path)


def add_path_to_PATH(path_to_add: str) -> None:
  # current_PATH: str = os.environ.get("PATH")
  # print_path(current_PATH)
  # input()
  if os.name == "nt":
    get_user_path_command: str = "reg query HKCU\\Environment /v PATH"
    overwrite_path_command: str = 'setx PATH "{path_content}"'
  elif os.name == "posix":
    get_user_path_command: str = ""
    overwrite_path_command: str = ""
    raise NotImplementedError
  else:
    raise OSError(f"your os {os.name} is not supported")

  # get only user path
  result = subprocess.run(
    get_user_path_command, 
    capture_output=True, 
    text=True,  # ensure str as output
    shell=True
  )
  output = result.stdout
  for line in output.splitlines():
    if "PATH" in line:
      user_PATH: str = line.split("    ")[-1]

  # add path to user path variable
  if path_to_add not in user_PATH:
    new_PATH: str = user_PATH + os.pathsep + path_to_add

    os.system(overwrite_path_command.format(path_content=new_PATH))


def ask_for_pw_two_times() -> str:
  while True:
    try:
      pw: str = getpass("Create PW password: ")
      pw_check: str = getpass("Confirm PW password: ")
    except KeyboardInterrupt:
      sys.exit()

    if pw == pw_check:
      return pw
    else:
      print("Error: passwords do not match. Try again\n")


if __name__ == "__main__":

  here: str = os.path.dirname(os.path.abspath(__file__))
  os.chdir(here)

  # create Commands folder
  os.mkdir(COMMANDS_COPY_FOLDER)

  # add Commands folder full path to PATH
  path_to_add: str = os.path.join(here, COMMANDS_COPY_FOLDER)
  add_path_to_PATH(path_to_add)

  # TODO create external function os indipendent like before
  # windows:
  # create copies (links do not work) to .exe commands files from 
  # venv\Scripts in the main project folder\Commands and then add that 
  # path to local PATH variable
  if os.name == "nt":
    for command in COMMANDS.keys():
      command_exe: str = f"{command}.exe"
      source_file: str = os.path.join(VENV_SCRIPTS_FOLDER_WIN, command_exe)
      link_name: str = os.path.join(COMMANDS_COPY_FOLDER, command_exe)
      
      # problems with links on windows
      # os.symlink(source_file, link_name)
      # copy the file
      with open(source_file, "rb") as file:
        content = file.read()
      with open(link_name, "wb") as file:
        file.write(content)

  # linux
  elif os.name == "posix":
    raise NotImplementedError

  else:
    raise OSError(f"your os {os.name} is not supported")
  
  
  
  # create usage_counter.json file
  couter_file: str = os.path.join(here, PACKAGE_NAME, COUNTER_JSON)
  if not os.path.exists(couter_file):
    with open(couter_file, "w") as jsonfile:
      json.dump(dict(), jsonfile)

  # create `pw/data/pw_objects.json` if it does not exists 
  # (otherwise passwords could be lost)
  pw_obj_full_path: str = os.path.join(here, PACKAGE_NAME, PW_OBJECTS)
  if not os.path.exists(pw_obj_full_path):
    # if it does not exist: create pw_objects.json as empty dictionary
    with open(pw_obj_full_path, "w") as jsonfile:
      json.dump(dict(), jsonfile)
  else:
    print(
      f"Cannot delete '{pw_obj_full_path}' file:"
      "it could contain some important data."
      "\nMove or delete it and restart setup"
    )
    sys.exit()

  # enter PW main password and use it for first encription
  print(
    "\nCreate your PW password:",
    "\n(this password will be asked everytime you use some encrypting /",
    "decrypting command)",
    "\n(DO NOT FORGET IT: it may not be changed if lost)\n",
  )
  pw: str = ask_for_pw_two_times()
  encrypt_msg = encrypt_str(os.getcwd(), pw, check=False)

  # create `pw/data/check_pw.txt` file and write the encrypted message
  check_pw_full_path: str = os.path.join(here, PACKAGE_NAME, CHECK_PW)
  with open(check_pw_full_path, "w") as txtfile:
    txtfile.write(encrypt_msg)