from data.utils import encrypt_str, decrypt_str, decrypt_str_list, generate_fernet_key
from data.strings import PW_OBJECTS, PW_CSV
from cryptography.fernet import Fernet
from getpass import getpass
import os, json



class PW (object):
  """
  Creates a PW object representing a single account. 

  If encrypted is false then pw is decrypted
  If encrypted is true then pw is encrypted

  """
  def __init__(self, site:str, username:str, email:str, pw:str, other:list[str], encrypted:bool=False):
    self.site = site
    self.username = username
    self.email = email
    if encrypted is False:
      self.encrypted_pw = encrypt_str(pw)
    elif encrypted is True:
      self.encrypted_pw = pw
    self.other = other


  def __eq__(self, other):
    """
    def: two PW objects are equal if "site", "username", "email" fields are equal
    """
    self_dict = self.__dict__
    other_dict = other.__dict__
    # `if self_dict["site"] == other_dict["site"] and self_dict["username"] == other_dict["username"] and self_dict["email"] == other_dict["email"]:`
    if all(self_dict[key] == other_dict[key] for key in ["site", "username", "email"]):
      return True
    return False
 

  def get_pw(self) -> str:
    return decrypt_str(self.encrypted_pw)


  def print_site(self) -> str:
    """
    Use this function to print only site information with username and email
    """
    return f" Sito: {self.site}\n Username: {self.username}\n Email: {self.email}"
 

  def print_site_pw(self, decrypted_pw:str=None) -> str:
    """
    Use this function to print all information linked to a site
    
    oss: use `decrypted_pw` equal as decrypted password for current object if known for skipping enter password
    """
    if decrypted_pw is None:
      decrypted_pw = decrypt_str(self.encrypted_pw)
    res = f" Sito: {self.site}\n Username: {self.username}\n Email: {self.email}\n Password: {decrypted_pw}\n Other:"
    # format 'other' section
    for el in self.other:
        res = res + f"\n  · {el}"
    return res


  def add_to_database(self) -> None:
    """
    Aggiunge l'oggetto self al database json in /Data/pw_objects.json
    """
    # load `pw_objects` as dictionary
    with open(PW_OBJECTS,"r") as jsonfile:
      pw_objects = json.load(jsonfile)

    # convert the object into a dictionary and 
    # add it to the list of values of `pw_objects`
    value = self.__dict__

    # if site in the database
    if self.site not in pw_objects.keys():  
      pw_objects[self.site] = [value]
      print("Correctly added pw to the database")
    # if site not in check if value alredy exists
    elif self.site in pw_objects.keys():
      # cannot use `if value not in pw_objects[self.site]` because same pw is encrypted differently
      # we will use PW object comparison defined without encrypted pw
      value_as_objects = [PW.from_dict(dict_obj) for dict_obj in pw_objects[self.site]]
      if self not in value_as_objects:
        pw_objects[self.site].append(value)
        print("Correctly added pw to the database")
      else:
        print("Could not add pw because it alredy exsists in database")
    # save changes
    with open(PW_OBJECTS, "w") as jsonfile:
      json.dump(pw_objects, jsonfile, indent=2)


  def remove_from_database(self) -> None:
    """
    Removes self object from the database in /Data/pw_objects.json
    Also if we are removing last object and the value of key site becomes
    an empty list, delete the key.
    """
    # load `pw_objects` as dictionary
    with open(PW_OBJECTS,"r") as jsonfile:
      pw_objects = json.load(jsonfile)

    # case site not in database
    if self.site not in pw_objects.keys():
      raise KeyError(f"Site {self.site} not in database")
    
    value = self.__dict__
    # remove object if found
    if value in pw_objects[self.site]:
      pw_objects[self.site].remove(value)
      print("Correctly removed object from database")
      # if it was last pw then del the site
      if pw_objects[self.site] == []:
        del(pw_objects[self.site])
        print("Correctly removed site from database because there was not any pw linked to it")
    else:
      print("Could not remove object from database because it does not exist")

    # save changes
    with open(PW_OBJECTS, "w") as jsonfile:
      json.dump(pw_objects, jsonfile, indent=2)
    

  def change_pw(self, new_pw:str=None) -> None:
    """
    Changes pw in self object and in database.
    """
    # Insert new password
    if new_pw is None:
      new_pw = getpass(prompt="Insert new password: ")
      new_pw_confirm = getpass(prompt="Confirm password: ")
      if new_pw != new_pw_confirm:
        raise ValueError("Error: passwords does not match")
    # encrypt new pw
    new_encrypt_str = encrypt_str(new_pw)
    # change pw in self object
    self.encrypted_pw = new_encrypt_str
    print("Password correctly changed in PW object")
    # change pw if self object in database
    with open(PW_OBJECTS,"r") as jsonfile:
      pw_objects = json.load(jsonfile)
    # base case
    if self.site not in pw_objects.keys():
      raise KeyError(f"Error: site {self.site} not in dataase")

    dict_list = pw_objects[self.site]
    for dic in dict_list:
      if dic["site"] == self.site and dic["username"] == self.username and dic["email"] == self.email:
        dic["encrypted_pw"] = new_encrypt_str
        print("Password changed correctly in database")
        # save changes
        with open(PW_OBJECTS, "w") as jsonfile:
          json.dump(pw_objects, jsonfile, indent=2)
        return
    print("Cannot change password in database because object not in database")




  @classmethod
  def from_dict(cls, data:dict[str,any]) -> 'PW':
    """
    Converts dictionary (well formatted or created with PW.__dict__())
    into a PW object
    """
    return cls(
      site = data['site'],
      username = data['username'],
      email = data['email'],
      pw = data['encrypted_pw'],
      other = data['other'],
      encrypted = True
    )




  # TODO other methods that replicates other files to "alleggerire" code e.g. copy pw from object, 
  # prints all objects, choose which account you want to copy pw, add pw to object 

  # TODO functions to add elements to pw_objects.json, encrypt and decrypt pw, print and so on.





def create_objects_from_json(site:str) -> list['PW']:
  """
  Returns the list of objects that are values of key site in pw_objects.json
  """
  # load `pw_objects` as dictionary
  with open(PW_OBJECTS,"r") as jsonfile:
    pw_objects = json.load(jsonfile)
  # site not in database
  if site not in pw_objects.keys():
    raise KeyError(f"site {site} not in database")
  else:
    # take value from key site in `pw_objects`
    value = pw_objects[site]
    # transform each pw dict in PW object
    for i, v in enumerate(value):
      value[i] = PW.from_dict(v)
  return value
    

def print_all_pw(site:str, print_pw=False) -> None:
  """
  Prints all objects linked as values in `pw_objects` from key `site`.
  If `print_pw=True` than prints more data (uses PW.print_site_pw)
  If `print_pw=False` than prints less data (uses PW.print_site)
  """
  # load `pw_objects` as dictionary
  with open(PW_OBJECTS,"r") as jsonfile:
    pw_objects = json.load(jsonfile)
  # site not in database
  if site not in pw_objects.keys():
    raise KeyError(f"site {site} not in database")
  
  if print_pw is True:
    encrypted_passwords = [pw_object.encrypted_pw for pw_object in create_objects_from_json(site)]
    decrypted_passwords = decrypt_str_list(encrypted_passwords)
    # uses print_site_pw without asking for pw
    for decrypted_pw, pw_object in zip(decrypted_passwords, create_objects_from_json(site)):
      print(pw_object.print_site_pw(decrypted_pw) + "\n")
    # remove passwords list
    del(decrypted_passwords)

  elif print_pw is False:
    for pw_object in create_objects_from_json(site):
      print(pw_object.print_site() + "\n")



def get_pw_from_json(site_query:str) -> str:
  """
  Input:
  · `site_query:str` is a part of the name of a site e.g. 'ith' -> 'github.com'

  Output:
  returns decrypted password from chosen username and email
  """
  sites = find_full_site_names(site_query)
  # base case: no sites found
  if sites == [""]:
    raise ValueError("No sites found")
  # rapid case: only one site found
  if len(sites) == 1:
    site = sites[0]
  # rapid case: site query is a full site name
  elif site_query in sites:
    site = site_query
  # general case: more than one site
  else:
    # enumerate sites and choose one
    for i, site in enumerate(sites):
      print(f" {i+1}. {site}")
    # ask for index
    selected_idx = int(input("\nSelect site number: ")) - 1
    site = sites[selected_idx]

  print(f"\nSite: {site}")
  # create pw obj list from chosen site
  obj_list = create_objects_from_json(site)
  # rapid case: a single pw linked to site
  if len(obj_list) == 1:
    obj = obj_list[0]
    print(obj.print_site())
    return obj_list[0].get_pw()
  # case with more accounts
  else:
    usernames = [obj.username for obj in obj_list]
    emails = [obj.email for obj in obj_list]
    # print choiches
    for i, (username, email) in enumerate(zip(usernames, emails)):
      print(f" {i+1}. username: {username}, email: {email}")
    # select account
    selected_index = int(input("\nSelect an account number: ")) - 1
    obj = obj_list[selected_index]
    print(obj.print_site())
    return obj.get_pw()


def copy_pw_from_json(site_query:str) -> None:
  """
  copies pw in the clipboard
  """
  # case no sites found
  try:
    pw = get_pw_from_json(site_query)
  except ValueError as e:
    print(e)
    return
  
  if os.name == "nt":
    os.system(f'echo {pw}| clip')
    print("\nPassword copied to clipboard")
  elif os.name == "posix":
    # TODO 
    print("TODO")


def find_full_site_names(site_query:str, show_print:bool=False) -> list[str]:
  """
  Input:
  · `site_query:str` is a part of the name of a site e.g. 'ith' -> 'github.com'
  · `show_print:bool=False` if true prints output in a nice way
  Output: list of all sites in `pw_objects.json` keys database that contain `site_query`
  """
  # load `pw_objects` as dictionary
  with open(PW_OBJECTS,"r") as jsonfile:
    pw_objects = json.load(jsonfile)
  # sites containing site_query in their name
  sites = [site for site in pw_objects.keys() if site_query in site]
  # case no sites
  if sites == []:
    # print("Zero sites found")
    return [""]
  # print case
  if show_print is True:
    for i,site in enumerate(sites):
      print(f"{i+1}. {site}")
  return sites


def create_csv_pw_file() -> None:
  """
  Create a csv file with all passwords
  """
  # load `pw_objects.json`
  with open(PW_OBJECTS, "r") as jsonfile:
    pw_objects = json.load(jsonfile)
  # raise error if file exists to avoid pw deletion
  if os.path.exists(PW_CSV):
    raise FileExistsError(f"File {PW_CSV} already exists. Delete or move it and retry")
  # generate key (i tried not to do this, but it is the fastest way)
  key = generate_fernet_key()
  # write on it
  with open(PW_CSV, "w") as csvfile:
    file_content = "site,username,email,password,other\n"
    for site in pw_objects:
      for pw_obj in create_objects_from_json(site):
        cur_pw = Fernet(key).decrypt(pw_obj.encrypted_pw.encode()).decode()
        other_str = ", ".join(pw_obj.other)
        file_content += f'"{pw_obj.site}","{pw_obj.username}","{pw_obj.email}","{cur_pw}","{other_str}"\n'
    # write content on it
    csvfile.write(file_content)
    # del some variables
    del(key); del(file_content); del(cur_pw)










if __name__ == "__main__":
  pass
  # create_csv_pw_file()
  # prova = PW("prova.com",None,"ciao@.com","ciaociao123",["my name is Iacopo","The code is 12346"])
  # prova.change_pw("pizzocalabro")
  # print(prova.print_site_pw())
  # prova.add_to_database()
  # prova.remove_from_database()
  # for k,v in a.items():
  #   print(k,v)
  # print_all_pw("prova.com",pw=True)
  # copy_pw_from_json("va")
