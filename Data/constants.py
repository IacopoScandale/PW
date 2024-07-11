from sys import exit
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from getpass import getpass
import os



DATA_FOLDER_NAME = "Data"
"""
Name of the folder containg config files etc
"""

PW_OBJECTS = os.path.join(DATA_FOLDER_NAME, "pw_objects.json")
"""
Relative path del file pw_objects.json
"""

PW_JSON = os.path.join(DATA_FOLDER_NAME, "pw.json")
"""
Relative path del file pw.json
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
Alias name calling ``
"""


def help_and_error(help_message:str, argv:list, argument_number:int=None) -> None:
  """
  Input
  -----
    * `help_message`: str multilinea contenente il messaggio di --help quando si scrive e.g.: "my_command --help"
    * `argv`: lista del modulo sys contenente gli argomenti
    * `argument_number`: exact number of arguments (if None it does not matter)
  
  Output 
  ------
    * Stampa il messaggio di help e blocca l'esecuzione del comando se si scrive 'nome_comando --help'
    * Stampa il messaggio di errore e blocca l'esecuzione del comando se si sbaglia il numero di argomenti
  """
  # help
  if len(argv) > 1 and (argv[1] == "--help" or argv[1] == "-h"):
    print(help_message)
    exit()
  # wrong arg number
  if argument_number is not None:
    if len(argv) != argument_number + 1:
      print(f"ERROR: Wrong Argument Number ({len(argv)-1} instead of {argument_number})")
      print("type 'command_name --help' for more info")
      exit()


def generate_fernet_key(passphrase:str=None):
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


def encrypt_str_list(decrypted_msg:list[str], pw:str=None, check:bool=True) -> list[str]:
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