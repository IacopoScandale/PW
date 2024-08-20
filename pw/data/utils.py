from .strings import CHECK_PW, COUNTER_JSON_NAME
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from getpass import getpass
import os
import sys
import json


def add_one_to_counter(command_name: str) -> None:
  """
  Call this function at the end of a command_file.py to
  add +1 usage to the counter. This counter will save
  how many times we use that command
  """
  here: str = os.path.dirname(os.path.abspath(__file__))
  full_path_counter_json: str = os.path.join(here, COUNTER_JSON_NAME)

  # create file if it does not exists
  if not os.path.exists(full_path_counter_json):
    print(f"Error: missing file {full_path_counter_json}")
    sys.exit()

  with open(full_path_counter_json, "r") as jsonfile:
    # load dictionary
    counter_json: dict[str,int] = json.load(jsonfile)
  # add +1 to the frequency dictionary
  if command_name not in counter_json:
    counter_json[command_name] = 1
  else:
    counter_json[command_name] += 1
  # save progress
  with open(full_path_counter_json, "w") as jsonfile:
    json.dump(counter_json, jsonfile, indent=2)


def generate_fernet_key(passphrase:str|None=None):
  """
  Derive a cryptographic key from a passphrase using PBKDF2 and then
  derive a Fernet key and write it into a key file
  
  Args
  ----
  - `passphrase` (str): The passphrase to derive the Fernet key from.

  Returns
  -------
  - bytes: The Fernet key.
  """
  if passphrase is None:
    passphrase = getpass(prompt="\nEnter PW password: ")
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt="salt".encode(),
    iterations=300000,
  )
  key = kdf.derive(passphrase.encode())
  fernet_key = urlsafe_b64encode(key)
  return fernet_key


def decrypt_str_list(encrypted_msg:list[str], pw:str=None) -> list[str]:
  """
  Decrypts a str `encrypted_msg`
  """
  try:
    key = generate_fernet_key(pw)
    return [Fernet(key).decrypt(msg.encode()).decode() for msg in encrypted_msg]
    # decrypted_msg = Fernet(key).decrypt(encrypted_msg.encode()).decode()
    # return decrypted_msg
  except:
    raise ValueError("wrong password")
    

def decrypt_str(encrypted_msg:str, pw:str=None) -> str:
  """
  cfr `decrypt_str_list`, but converts a single str instead of list[str]
  """
  return decrypt_str_list([encrypted_msg], pw)[0]


def encrypt_str_list(decrypted_msg:list[str], pw:str|None=None, check:bool=True) -> list[str]:
  """
  Encrypts a str `decrypted_msg`, but first checks if pw is correct
  using `check_pw` function.

  Input:
  · `decrypted_msg:list[str]` list of decrypted strings to encrypt 
  · `pw:str=None` if None this funcion ask user to insert pw, otherwise uses arg `pw` if `pw` is not None
  · `check:bool=True` if true calls `check_pw` function, otherwise it does not

  Returns: the list of encrypted strings
  """
  # ask user for password if pw is None
  if pw is None:
    pw = getpass(prompt="\nEnter PW password: ")
  # check if pw is correct
  if check is True:
    if check_pw(pw) is False:
      raise ValueError("wrong password")
  # try to return encrypted_msg
  try:
    key = generate_fernet_key(pw)
    return [Fernet(key).encrypt(msg.encode()).decode() for msg in decrypted_msg]
    # encrypted_msg = Fernet(key).encrypt(decrypted_msg.encode()).decode()
    # return encrypted_msg
  except:
    raise ValueError("Error: wrong password")


def encrypt_str(decrypted_msg:str, pw:str=None, check:bool=True) -> str:
  """
  cfr encrypt_str_list, but converts a single str instead of a list[str]
  """
  return encrypt_str_list([decrypted_msg], pw, check)[0]


def check_pw(pw:str) -> bool:
  """
  Use this function to check if a password pw is correct.
  Pw is correct when it can decode `check_pw.txt` encrypted
  message.

  Returns true if pw is correct, false otherwise.
  """
  # open encrypted str
  with open(CHECK_PW, "r") as txtfile:
    encrypted_msg = txtfile.read()
  # try decrypt `check_pw.txt`
  try:
    decrypt_str(encrypted_msg, pw)
    return True
  except:
    return False  