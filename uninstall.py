"""
Run this from project folder from terminal as Administrator
"""

import os, sys, json
from Data.constants import CONFIG_JSON, COMMANDS_BAT, COMMANDS_SH, CHECK_PW, PW_OBJECTS, OLD_PW_OBJECTS


# title
print("=================================")
print("||        PW UNINSTALL         ||")
print("=================================",end="\n\n")

# info
print("This uninstaller is going only to un-do 'setup.py'")
print("It requires to be run as Administrator! otherwise uninstall cannot be fully completed")
print(f"Moreover file '{PW_OBJECTS}' will be kept and renamed as '{OLD_PW_OBJECTS}',")
print("in this way pw data will be preserved (but passwords will be encrypted with your previous PW password!)\n")


# Ask if path is correct
print("Make sure the following path is the same of PW folder you want to uninstall")
ask = input(f"`{os.getcwd()}` is the correct path?\n [Y,n]: ")
if ask not in "sSyY":
  print("Run this script in the correct path as administrator")
  sys.exit()


# delete files `check_pw.txt` and `config.json`
if os.path.exists(CONFIG_JSON):
  os.remove(CONFIG_JSON)
if os.path.exists(CHECK_PW):
  os.remove(CHECK_PW)

# rename file `pw_objects.json` for not loosing data
if os.path.exists(PW_OBJECTS):
  os.rename(PW_OBJECTS, OLD_PW_OBJECTS)

# windows
if os.name == "nt": 
  # commands.bat full path
  # add one " for being sure that paths that contain spaces will be supported (in regedit it will write exactly "path" with one ")
  commands_bat_full_path_str = f'"{os.path.join(os.getcwd(), COMMANDS_BAT)}"'

  # get regedit AutoRun paths Values in Command Processor
  tmp_file_path = "tmp.txt"
  os.system(f'reg query "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun > "{tmp_file_path}"')

  # read tmpfile and get all paths in AutoRun
  with open(tmp_file_path, "r") as txtfile:
    lines = txtfile.readlines()
  # delete the tmp file
  os.remove(tmp_file_path)
  # find existing paths
  for line in lines:
    if "AutoRun" in line:
      # get the list of all paths in value "AutoRun"
      paths = line[21:].strip().split(" & ")

      # get the list of all paths in value "AutoRun"
      paths_in_line = line[21:].strip()
      if paths_in_line == "": # case: no paths
        paths = []
      elif " & " in paths_in_line: # case: more than a path
        paths = paths_in_line.split(" & ")
      else: # case: a single path
        paths = [paths_in_line]

  # remove commands.bat file full path from the values
  if paths != []:
    paths.remove(commands_bat_full_path_str)

  # join all paths separated by &
  concatenated_paths = " & ".join(paths)
  # print(concatenated_paths)
  os.system(f'reg add "HKLM\\SOFTWARE\\Microsoft\\Command Processor" /v AutoRun /t REG_SZ /d "{concatenated_paths}" /f')

  # delete `commands.bat`
  if os.path.exists(COMMANDS_BAT):
    os.remove(COMMANDS_BAT)






# linux
elif os.name == "posix":











  # delete `commands.bat`
  os.remove(COMMANDS_BAT)
  # TODO