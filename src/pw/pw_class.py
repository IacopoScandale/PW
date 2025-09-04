import json
import sys
import time
from typing import Any

from cryptography.fernet import Fernet
import pyperclip
from rich import print

from .data.strings import FILE_PW_CSV, FILE_PW_OBJECTS_JSON
from .data.utils import (
    ask_for_pw_two_times,
    decrypt_str,
    decrypt_str_list,
    encrypt_str,
    generate_fernet_key,
    get_edit_date,
)


class PW(object):
    """
    Creates a PW object representing a single account.

    If encrypted is false then pw is decrypted
    If encrypted is true then pw is encrypted

    """

    def __init__(
        self,
        site: str,
        username: str,
        email: str,
        pw: str,
        other: list[str],
        encrypted: bool = False,
        edit_date: str | None = None,
    ):
        self.site = site
        self.username = username
        self.email = email
        if not encrypted:
            self.encrypted_pw = encrypt_str(pw)
        elif encrypted:
            self.encrypted_pw = pw
        self.other = other
        self.edit_date = edit_date

    def __eq__(self, other):
        """
        def: two PW objects are equal if "site", "username", "email" fields
        are equal
        """
        self_dict = self.__dict__
        other_dict = other.__dict__

        if all(
            self_dict[key] == other_dict[key] for key in ["site", "username", "email"]
        ):
            return True
        return False

    def get_pw(self) -> str:
        return decrypt_str(self.encrypted_pw)

    def print_site(self) -> str:
        """
        Use this function to print only site information with username
        and email
        """
        return (
            f"· Site:      {self.site}\n"
            f"  Username:  {self.username}\n"
            f"  Email:     {self.email}\n"
            f"  Last Edit: {self.edit_date}\n"
        )

    def print_site_pw(self, decrypted_pw: str | None = None) -> str:
        """
        Use this function to print all information linked to a site

        oss: use `decrypted_pw` equal as decrypted password for current
             object if known for skipping enter password
        """
        if decrypted_pw is None:
            decrypted_pw = decrypt_str(self.encrypted_pw)
        res: str = (
            f"· Site:      {self.site}\n"
            f"  Username:  {self.username}\n"
            f"  Email:     {self.email}\n"
            f"  Last Edit: {self.edit_date}\n"
            f"  Password:  {decrypted_pw}\n"
            "  Other:"
        )
        # format 'other' section
        for el in self.other:
            res = res + f"\n    · {el}"
        return res

    def add_to_database(self) -> None:
        """
        Aggiunge l'oggetto self al database json in /Data/pw_objects.json
        """
        # load `pw_objects` as dictionary
        with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
            pw_objects = json.load(jsonfile)

        # convert the object into a dictionary and add it to the list of
        # values of `pw_objects`
        value = self.__dict__

        # if site in the database
        if self.site not in pw_objects.keys():
            pw_objects[self.site] = [value]
            print("\nCorrectly added pw to the database")
        # if site not in check if value already exists
        elif self.site in pw_objects.keys():
            # cannot use `if value not in pw_objects[self.site]` because same
            # pw is encrypted differently
            # we will use PW object comparison defined without encrypted pw
            value_as_objects = [
                PW.from_dict(dict_obj) for dict_obj in pw_objects[self.site]
            ]
            if self not in value_as_objects:
                pw_objects[self.site].append(value)
                print("\nCorrectly added pw to the database")
            else:
                print("\nCould not add pw because it already exists in database")
        # save changes
        with open(FILE_PW_OBJECTS_JSON, "w") as jsonfile:
            json.dump(pw_objects, jsonfile, indent=2)

    def remove_from_database(self) -> None:
        """
        Removes self object from the database in /Data/pw_objects.json
        Also if we are removing last object and the value of key site becomes
        an empty list, delete the key.
        """
        # load `pw_objects` as dictionary
        with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
            pw_objects = json.load(jsonfile)

        # case site not in database
        if self.site not in pw_objects.keys():
            print(f"Site {self.site} not in database")
            sys.exit()

        value = self.__dict__
        # remove object if found
        if value in pw_objects[self.site]:
            print(self.print_site())
            try:
                ask: str = input("Do you want to remove it?\n  [Y,n]: ")
            except KeyboardInterrupt:
                sys.exit()
            if ask in "yY":
                pw_objects[self.site].remove(value)
                print("Correctly removed object from database")
                # if it was last pw then del the site key
                if pw_objects[self.site] == []:
                    del pw_objects[self.site]
        else:
            print("Could not remove object from database because it does not exist")

        # save changes
        with open(FILE_PW_OBJECTS_JSON, "w") as jsonfile:
            json.dump(pw_objects, jsonfile, indent=2)

    def edit(
        self,
        new_site: str | None = None,
        new_email: str | None = None,
        new_username: str | None = None,
        change_pw: bool = False,
        edit_other: bool = False,
    ) -> None:
        """
        Lets the user edit specific fields of pw object and refreshes edit
        date
        """
        # base case: exit if there is nothing to edit
        if not any([new_site, new_email, new_username, change_pw, edit_other]):
            return

        with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
            pw_objects: dict = json.load(jsonfile)

        for dic in pw_objects[self.site]:
            if (
                dic["site"] == self.site
                and dic["username"] == self.username
                and dic["email"] == self.email
            ):
                if new_site and not new_site == self.site:
                    print(
                        f"[underline]Changed Site Name[/underline] from '{self.site}' to '{new_site}'"
                    )
                    # without changing anything to self, get self position in
                    # pw_objects[self.site] list to then change key
                    site_objects: list[dict] = pw_objects[self.site]
                    pw_object_pos: int = site_objects.index(dic)
                    dic["site"] = new_site
                if new_username:
                    print(
                        f"[underline]Changed Username[/underline] from '{self.username}' to '{new_username}'"
                    )
                    self.username = new_username
                    dic["username"] = new_username
                if new_email:
                    print(
                        f"[underline]Changed Email[/underline] from '{self.email}' to '{new_email}'"
                    )
                    self.email = new_email
                    dic["email"] = new_email
                if change_pw:
                    print("\n[underline]Change Site Password[/underline]")
                    new_pw: str = ask_for_pw_two_times("New password: ", hide_password=False)
                    new_encrypted_pw = encrypt_str(new_pw)
                    self.encrypted_pw = new_encrypted_pw
                    dic["encrypted_pw"] = new_encrypted_pw

                if edit_other:
                    print("\n[underline]Edit Other Infos[/underline]")
                    # edit existing other
                    new_other: list[str] = []
                    for i, other in enumerate(dic["other"], 1):
                        if i == 1:
                            print(
                                "Choices are\n· [green]k[/green] — [bright_black]keep item[/bright_black]\n· [red]d[/red] — [bright_black]delete item[/bright_black]\n· [yellow]e[/yellow] — [bright_black]edit item[/bright_black]"
                            )
                        print(f"\n{i:>3}. [green]{other}[/green]")
                        try:
                            cur_choice: str = input("      [K,d,e]: ")
                        except KeyboardInterrupt:
                            sys.exit()

                        edited_other: str = edit_recursive_choices(cur_choice, other)
                        if edited_other:
                            new_other.append(edited_other)

                        # add newline in the last step (just for gui)
                        if i == len(dic["other"]) - 1:
                            print()

                    # add new other
                    print("Enter additional infos:")
                    print("[bright_black](leave blank to stop)[/bright_black]")
                    while True:
                        try:
                            info: str = input("  · ")
                        except KeyboardInterrupt:
                            sys.exit()
                        if not info.strip():
                            break
                        else:
                            new_other.append(info.strip())

                    dic["other"] = new_other
                    self.other = new_other

                edit_date: str = get_edit_date()
                dic["edit_date"] = edit_date

                # also change pw_object key (cfr PW_OBJECTS)
                if new_site and not new_site == self.site:
                    if new_site not in pw_objects:
                        pw_objects[new_site] = []

                    # if only one element (i.e. self) then remove site 
                    # key from PW_OBJECTS
                    if len(site_objects) == 1:
                        pw_objects.pop(self.site)
                    else:
                        # remove self from old site key
                        pw_objects[self.site].pop(pw_object_pos)

                    self.site = new_site
                    self.edit_date = edit_date
                    pw_objects[new_site].append(self.__dict__)

        # write changes
        with open(FILE_PW_OBJECTS_JSON, "w") as jsonfile:
            json.dump(pw_objects, jsonfile, indent=2)

        print("\nChanges done:")
        print(self.print_site())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PW":
        """
        Converts dictionary (well formatted or created with PW.__dict__())
        into a PW object
        """
        return cls(
            site=data["site"],
            username=data["username"],
            email=data["email"],
            pw=data["encrypted_pw"],
            other=data["other"],
            encrypted=True,
            edit_date=data.get("edit_date", None),
        )


# TODO or maybe not, some of the following functions are redundant. Some
# of them could be rewritten using `get_pw_obj_from_site_query`


def create_objects_from_json(site: str) -> list["PW"]:
    """
    Returns the list of objects that are values of key site in
    pw_objects.json
    """
    # load `pw_objects` as dictionary
    with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
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


def print_all_pw(site: str, print_pw: bool = False) -> None:
    """
    Prints all objects linked as values in `pw_objects` from key `site`.
    If `print_pw=True` than prints more data (uses PW.print_site_pw)
    If `print_pw=False` than prints less data (uses PW.print_site)
    """
    # load `pw_objects` as dictionary
    with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
        pw_objects = json.load(jsonfile)
    # site not in database
    if site not in pw_objects.keys():
        raise KeyError(f"site {site} not in database")

    if print_pw is True:
        encrypted_passwords = [
            pw_object.encrypted_pw for pw_object in create_objects_from_json(site)
        ]
        decrypted_passwords = decrypt_str_list(encrypted_passwords)
        # uses print_site_pw without asking for pw
        for decrypted_pw, pw_object in zip(
            decrypted_passwords, create_objects_from_json(site)
        ):
            print(pw_object.print_site_pw(decrypted_pw) + "\n")
        # remove passwords list
        del decrypted_passwords

    elif print_pw is False:
        for pw_object in create_objects_from_json(site):
            print(pw_object.print_site() + "\n")


def get_pw_from_json(site_query: str) -> str:
    """
    Input:
    · `site_query:str` is a part of the name of a site
       e.g., 'ith' -> 'github.com'

    Output:
    returns decrypted password from chosen username and email
    """
    sites = find_full_site_names(site_query)
    # base case: no sites found
    if sites == [""]:
        print(f"No sites found containing query: '{site_query}'")
        sys.exit()
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
            print(f" {i + 1}. {site}")
        # ask for index
        try:
            selected_idx = int(input("\nSelect site number: ")) - 1
        except KeyboardInterrupt:
            sys.exit()
        site = sites[selected_idx]

    print(f"\nSite: {site}")
    # create pw obj list from chosen site
    obj_list = create_objects_from_json(site)
    # rapid case: a single pw linked to site
    if len(obj_list) == 1:
        obj = obj_list[0]
    # case with more accounts
    else:
        usernames = [obj.username for obj in obj_list]
        emails = [obj.email for obj in obj_list]
        # print choices
        for i, (username, email) in enumerate(zip(usernames, emails)):
            print(f" {i + 1}. username: {username}, email: {email}")
        # select account
        try:
            selected_index = int(input("\nSelect an account number: ")) - 1
        except KeyboardInterrupt:
            sys.exit()
        obj = obj_list[selected_index]

    print(obj.print_site())
    return obj.get_pw()


def copy_pw_from_json(site_query: str) -> None:
    """
    copies pw in the clipboard
    """

    pw = get_pw_from_json(site_query)

    # copy pw to the clipboard for 30 seconds
    try:
        pyperclip.copy(pw)
        print("\nPassword copied to the clipboard")
        print("[bright_black]It will be cleared in 15 seconds or with Ctrl+C (^C)[/bright_black]")
        time.sleep(15)

    # exit with KeyboardInterrupt
    except KeyboardInterrupt:
        sys.exit()

    # clear sensitive data no matter what
    finally:
        pyperclip.copy("")
    
    # if os.name == "nt":
    #     os.system(f'echo "{pw}"| clip')
    # elif os.name == "posix":
    #     os.system(f'echo -n "{pw}"| xclip -selection clipboard')
    #     print("\nPassword copied to clipboard")


def find_full_site_names(
    site_query: str, 
    show_print: bool = False,
    raw_print: bool = False,
) -> list[str]:
    """
    Input:
    · `site_query:str` is a part of the name of a site
       e.g. 'ith' -> 'github.com'
    · `show_print:bool=False` if true prints output in a nice way
    Output: list of all sites in `pw_objects.json` keys database that
            contain `site_query`
    """
    # load `pw_objects` as dictionary
    with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
        pw_objects = json.load(jsonfile)
    # sites containing site_query in their name
    sites = [site for site in pw_objects.keys() if site_query in site]
    # case no sites
    if sites == []:
        # print("Zero sites found")
        return [""]
    # print case
    if show_print is True:
        for i, site in enumerate(sites, 1):
            if raw_print:
                print(site)
            else:
                print(f"{i:>5}. {site}")
    return sites


# TODO NotImplemented
def create_csv_pw_file() -> None:
    """
    Create a csv file with all passwords
    """
    # load `pw_objects.json`
    with open(FILE_PW_OBJECTS_JSON, "r") as jsonfile:
        pw_objects = json.load(jsonfile)
    # raise error if file exists to avoid pw deletion
    if FILE_PW_CSV.exists():
        raise FileExistsError(
            f"File {FILE_PW_CSV} already exists. Delete or move it and retry"
        )
    # generate key (i tried not to do this, but it is the fastest way)
    key = generate_fernet_key()
    # write on it
    with open(FILE_PW_CSV, "w") as csvfile:
        file_content = "site,username,email,password,other\n"
        for site in pw_objects:
            for pw_obj in create_objects_from_json(site):
                cur_pw = Fernet(key).decrypt(pw_obj.encrypted_pw.encode()).decode()
                other_str = ", ".join(pw_obj.other)
                file_content += f'"{pw_obj.site}","{pw_obj.username}","{pw_obj.email}","{cur_pw}","{other_str}"\n'
        # write content on it
        csvfile.write(file_content)
        # del some variables
        del key
        del file_content
        del cur_pw


def print_site_info_command(site_query: str, all_info: bool = False) -> None:
    sites = find_full_site_names(site_query)

    # case no sites found
    if sites == [""]:
        print("\nNo sites found in the database")
        sys.exit()

    # rapid case when site_query == site
    if site_query in sites:
        site = site_query
        # print site accounts
        print_all_pw(site, all_info)

    # rapid case when there is only one site found in sites
    elif len(sites) == 1:
        site = sites[0]
        ask = input(f"{site}?\n [Y,n]: ")
        if ask in "yYsS":
            # print site accounts
            print_all_pw(site, all_info)

    else:
        # enumerate all sites
        for i, site in enumerate(sites, 1):
            print(f"{i:>5}. {site}")

        # ask for index
        try:
            selected_idx = int(input("\nSelect site number: ")) - 1
        except KeyboardInterrupt:
            sys.exit()
        site = sites[selected_idx]
        # print site accounts
        print_all_pw(site, all_info)


def get_pw_obj_from_site_query(site_query: str) -> PW:
    """
    New approach:
    TODO change older functions to use this one: first get the object,
    then apply methods to it
    """
    sites = find_full_site_names(site_query)
    # base case: no sites found
    if sites == [""]:
        print(f"No sites found containing query: '{site_query}'")
        sys.exit()
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
            print(f" {i + 1}. {site}")
        # ask for index
        try:
            selected_idx = int(input("\nSelect site number: ")) - 1
        except KeyboardInterrupt:
            sys.exit()
        site = sites[selected_idx]

    print(f"\nSite: {site}")
    # create pw obj list from chosen site
    obj_list = create_objects_from_json(site)
    # rapid case: a single pw linked to site
    if len(obj_list) == 1:
        pw_obj = obj_list[0]
    # case with more accounts
    else:
        usernames = [obj.username for obj in obj_list]
        emails = [obj.email for obj in obj_list]
        # print choices
        for i, (username, email) in enumerate(zip(usernames, emails)):
            print(f" {i + 1}. username: {username}, email: {email}")
        # select account
        try:
            selected_index = int(input("\nSelect an account number: ")) - 1
        except KeyboardInterrupt:
            sys.exit()
        pw_obj = obj_list[selected_index]

    return pw_obj


def edit_recursive_choices(choice: str, other: str) -> str:
    """
    cfr pw_class edit method
    """
    if choice in "Kk":
        return other
    elif choice in "dD":
        return ""
    elif choice in "eE":
        try:
            return input("Edit other: ")
        except KeyboardInterrupt:
            sys.exit()
    else:
        return edit_recursive_choices(choice, other)