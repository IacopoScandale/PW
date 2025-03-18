from .data.utils import add_one_to_counter, get_edit_date, check_pw
from .data.strings import PW_ADD_COMM_NAME
from .pw_class import PW
import sys


def add_comm() -> None:
  """
  TODO
  """
  # ask manually for account info
  try:
    site: str = input(f'{"Enter site: ":>17}')
    username: str = input(f'{"Username: ":>17}')
    email: str = input(f'{"Email: ":>17}')
    # while True:
    pw: str = input(f'{"Site password: ":>17}')
      # if check_pw(pw):
        # break
  except KeyboardInterrupt:
    sys.exit()

  other: list[str] = []
  print("  \nEnter other private infos:")
  print("  (leave blank to stop)")

  while True:
    try:
      info: str = input("   · ")
      if info.strip() == "":
        break
      else:
        other.append(info.strip())
    except KeyboardInterrupt:
      sys.exit()

  # create obj and add to database
  pw_obj = PW(
    site, username, email, pw, other, encrypted=False, edit_date=get_edit_date()
  )
  pw_obj.add_to_database()

  # show some data
  print(pw_obj.print_site())

  add_one_to_counter(PW_ADD_COMM_NAME)