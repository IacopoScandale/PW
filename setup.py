import os, sys, json
from data.utils import encrypt_str
from data import strings
from getpass import getpass
"""
PW Setup: Call this file as Administrator!

Windows: double click on setup.py or call from terminal
Linux: call this file from terminal
"""

# title
print("=================================")
print("||          PW SETUP           ||")
print("=================================",end="\n\n")


# install location
# get the full path of this file
this_file_full_path = os.path.abspath(__file__)
# get full path of project folder
main_folder_full_path = os.path.dirname(this_file_full_path)
# move to that directory
os.chdir(main_folder_full_path)


# create virtual environment
if not os.path.exists("venv"):
  print("Creating Virtual Environment 'venv'...")
  os.system(f"{sys.executable} -m venv venv")  
  print("Done!\n")



# create `Data/pw_objects.json` if it does not exists (otherwise passwords could be lost)
if not os.path.exists(strings.PW_OBJECTS):
  # if it does not exist: create pw_objects.json as empty dictionary
  with open(strings.PW_OBJECTS, "w") as jsonfile:
    json.dump(dict(), jsonfile)
else:
  print("Cannot delete 'pw_objects.json' file: it could contain some important data.\nMove or delete it and restart setup")
  sys.exit()


# # write path in `Data/config.json` dict
# config = dict()
# config["main folder path"] = os.getcwd()
# # save json config file
# with open(CONFIG_JSON, "w") as jsonfile:
#   json.dump(config, jsonfile, indent=2)


# install from requirements.txt in virtual environment
print("\nInstalling Dependencies...")
if os.name == "nt": # Windows
  os.system(f"{strings.PIP_VENV_WIN} install -r requirements.txt")
  print("Done!\n")
elif os.name == "posix":
  os.system(f"{strings.PIP_VENV_LINUX} install -r requirements.txt")
  print("Done!\n")

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
encrypt_msg = encrypt_str(os.getcwd(), pw, check=False)
# create `check_pw.txt file`
with open(strings.CHECK_PW, "w") as txtfile:
  # write some encrypted text
  txtfile.write(encrypt_msg)



# TODO create .bat and .sh aliases files
# Windows Setup
if os.name == "nt":
  python_venv_full_path = os.path.join(os.getcwd(), strings.PYTHON_VENV_WIN)


  def windows_alias_command_line(command_name:str, filename_py:str, args:str="") -> str:
    """
    Create windows command line for file comands.bat
    Input:
    - `filename_py:str` name of the python file to call
    - `command_name:str` name of the alias
    - `args:str=""` insert other default arguments (separated by a space) if needed
    """
    command_file_path = os.path.join(os.getcwd(), filename_py)
    return f"doskey {command_name} = {python_venv_full_path} {command_file_path} {args} $*\n"


  # windows echo off
  commands = "@echo off\n\n"
  # pw.add command
  commands += windows_alias_command_line(strings.PW_ADD_COMM_NAME, "pw_add.py")
  # pw.info command
  commands += windows_alias_command_line(strings.PW_INFO_COMM_NAME, "pw_site_info.py", args="False")
  # pw.all_info command
  commands += windows_alias_command_line(strings.PW_ALL_INFO_COMM_NAME, "pw_site_info.py", args="True")
  # copy pw to clipboard
  commands += windows_alias_command_line(strings.PW_COPY_SITE_PW, "pw_copy.py")
  # pw help
  commands += windows_alias_command_line(strings.PW_HELP, "pw_help.py")

  # TODO add more commands
  print("Done!\n")  

  
  # Write commands on commands.bat file
  with open(strings.COMMANDS_BAT, "w") as txtfile:
    txtfile.write(commands)


  # Regedit Part
  # path is inside \"...\" because in this way paths containing spaces are supported
  print("Adding commands to regedit AutoRun...")
  commands_bat_full_path_str = f'\\"{os.path.join(os.getcwd(), strings.COMMANDS_BAT)}\\"'
  
  # add automatically commands.bat file to regedit AutoRun Value in Command Processor
  tmp_file_path = "tmp.txt"
  try:
    os.system(f'reg query "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun > "{tmp_file_path}"')
  except:
    print("Error: you must run this script as administrator")
    sys.exit()

  # read tmpfile and get all paths in AutoRun
  with open(tmp_file_path, "r") as txtfile:
    lines = txtfile.readlines()
  # delete the tmp file
  os.remove(tmp_file_path)
  # find existing paths
  for line in lines:
    if "AutoRun" in line:
      # get the list of all paths in value "AutoRun"
      paths = line[21:].strip().split("&")
      # base case if no paths in regedit AutoRun: otherwise then " & ".join(paths)
      # joins "" and break windows terminal
      if paths == [""]:
        paths = []
      

  # if a path starts and ends with ", we must add \ in front of "
  for i, path in enumerate(paths):
    # strip every path: it could contain spaces because we are splitting with "&"
    # but each path could be separated with " & "
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
      # add \ in front of each "
      path = f'\\"{path[1:-1]}\\"'
    # refresh path in paths list
    paths[i] = path


  # add commands.bat file full path to the values
  if commands_bat_full_path_str not in paths:
    paths.append(commands_bat_full_path_str)

  # join all paths separated by &
  concatenated_paths = " & ".join(paths)
  # print(concatenated_paths)
  os.system(f'reg add "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun /t REG_SZ /d "{concatenated_paths}" /f')

  print("Done!\n")


# linux and (i hope :) macOS Setup
elif os.name == "posix":
  # TODO
  pass





  # TODO add automatically file to current shell.rc

else:
  raise OSError(f"Your os {os.name} is not supported")




print("PW setup has been completed successfully.")