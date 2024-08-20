from pw.data.strings import *
import subprocess
import os
import sys


def print_path(path: str) -> None:
  paths: list[str] = path.split(os.pathsep)
  for path in paths:
    print(path)


def remove_folder(folder: str) -> None:
  """
  Recursively deletes a folder and all folders and files inside
  """
  if os.name == "nt":
    command: str = 'rmdir /s /q "{folder}"'
  elif os.name == "posix":
    command: str = 'rm -rf {folder}'
  else:
    raise OSError(f"your os {os.name} is not supported")

  os.system(command.format(folder=folder))


def remove_paths_from_PATH(path_to_remove: str) -> None:
  """
  Removes `path_to_remove` from local PATH variable
  """
  # current_PATH: str = os.environ.get('PATH', '')
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

  # add path and update variable
  paths: list[str] = user_PATH.split(os.pathsep)
  paths = [p for p in paths if p != path_to_remove]
  new_PATH: str = os.pathsep.join(paths)
  
  os.system(overwrite_path_command.format(path_content=new_PATH))




if __name__ == "__main__":
  # info
  print(
    f"NB: file '{os.path.join(PACKAGE_NAME, PW_OBJECTS)}' will be",
    f"kept and renamed as '{os.path.join(PACKAGE_NAME, OLD_PW_OBJECTS)}'"
    "\nIn this way pw data will be preserved (but passwords remains",
    "encrypted with your previous PW password!)\n"
  )
  
  here: str = os.path.dirname(os.path.abspath(__file__))
  os.chdir(here)

  # remove directories
  if os.path.exists(COMMANDS_COPY_FOLDER):
    remove_folder(COMMANDS_COPY_FOLDER)
  if os.path.exists(VENV_FOLDER):
    remove_folder(VENV_FOLDER)
  if os.path.exists(INFO_FOLDER):
    remove_folder(INFO_FOLDER)

  # remove Commands from PATH
  path_to_remove: str = os.path.join(here, COMMANDS_COPY_FOLDER)
  remove_paths_from_PATH(path_to_remove)


  # delete file `check_pw.txt`
  check_pw_full_path: str = os.path.join(here, PACKAGE_NAME, CHECK_PW)
  if os.path.exists(check_pw_full_path):
    os.remove(check_pw_full_path)

  # if exists old_pw_objects exit and do not overwrite it
  old_pw_obj_full_path: str = os.path.join(here, PACKAGE_NAME, OLD_PW_OBJECTS)
  if os.path.exists(old_pw_obj_full_path):
    print(f"ERROR: file {old_pw_obj_full_path} already exists.")
    print("If you want to uninstall PW move or delete that file")
    sys.exit()

  # rename file `pw_objects.json` for not loosing data
  pw_obj_full_path: str = os.path.join(here, PACKAGE_NAME, PW_OBJECTS)
  if os.path.exists(pw_obj_full_path):
    os.rename(pw_obj_full_path, old_pw_obj_full_path)