# PW - CLI Password Manager

Command-line password manager to securely store, copy and manage site accounts passwords.

## Table of Contents
- [Installation (Pip)](#pip-installation)
  - [Virtual env installation](#virtual-env-installation)
- [Uninstall](#uninstall)
- [Usage](#usage)
  - [Available Commands](#available-commands)
  - [Usage Examples](#usage-examples)
    - [Display some infos](#1-display-some-infos)
    - [Add a new account](#add-a-new-account)
    - [Retrieve information about a site](#retrieve-information-about-a-site)
    - [View all information about a site (requires password)](#view-all-information-about-a-site-requires-password)
    - [Copy an account password to the clipboard](#copy-an-account-password-to-the-clipboard)
    - [List all saved sites](#list-all-saved-sites)
    - [Edit an account](#edit-an-account)
    - [Remove an account](#remove-an-account)
- [Security Notes](#security-notes)
- [License](#license)
- [TODO](#todo)


## Pip Installation

Installation is through pip and it is cross-platform for Linux and Windows.

Since it only requires `cryptography==42.0.5` the easiest way is install in global pip environment: download the project, open a terminal, move into the main folder and use the following command:
```sh
pip install .
```
or for editable mode:
```sh
pip install -e .
```
Make sure python env is on path so you can use `pw` command in every shell

### Virtual env installation
If you do not want to install in the base pip env you can create a virtual environment e.g. with venv: always in the main project folder run:
```sh
python -m venv venv

# linux
source venv/bin/activate
# windows
venv\Scripts\activate

pip install .  # -e for editable mode
```
Then if you want those commands in every shell put on path only the pw command inside the scripts folder in venv. Do not put the whole folder on path because it also contains other scripts like python or pip that will overwrite the default ones.

You can copy pw scripts file somewhere else in another folder on path (e.g. /usr/local/bin for linux)

> For Linux: `xclip` is required for copying passwords into the clipboard.

## Uninstall
Since it is a pip managed python package just use the following: (as installation, navigate into therminal at the main progect folder)

```sh
pip uninstall .
```

If you did some other things to install for example virtual evironments or other, just undo them.


## Usage

The basic command to run PW2 is:

```sh
pw [command] [options]
```

You can use the command without anything to show a 

You can type the following to get help
```sh
pw -h
```

### Available Commands

| [command]      | Description |
|-------------|------------|
| `add`       | Adds a new account to the database. |
| `info`      | Shows information related to a specific account (search by site). |
| `all_info`  | Prints all information related to a specific account (requires PW password). |
| `copy`      | Copies the password of the selected account to the clipboard. |
| `list`      | Lists all sites stored in the database (supports filtering by site query). |
| `edit`      | Finds an account by site query and allows you to edit its information. |
| `remove`    | Finds an account by site query and removes it. |

### Usage Examples

#### 1. Display some infos
You can use the package name without any parameter to show the following infos:
```sh
pw

commands:               times used:
——————————————————————————————————————
   1. add                        6
   2. info                       1
   3. all_info                  11
   4. copy                       5
   5. list                      12
   6. edit                      18
   7. remove                     3
——————————————————————————————————————
      Total:                    56
```

#### Add a new account
```sh
pw add
```
The program will prompt you to enter the account details.

#### Retrieve information about a site
If we know that github.com is on our pw local database, we can use
```sh
pw info git 
```
And all github accounts will we printed (without password of course). 

#### View all information about a site (requires password)
If you want to print all information, password included you need to use:
```sh
pw all_info git
```
That requires PW main password

#### Copy an account password to the clipboard
```sh
pw copy git
```

#### List all saved sites
```sh
pw list
```

#### Edit an account
For example let's change the github email for a selected account (you can store all'your different github accounts of course and then choose the one to edit) and site password
```sh
pw edit "hub" --email new@mail --change-pw
```
You can see all other options with `pw edit -h`
#### Remove an account
```sh
pw remove github.com
```


## Security Notes
- All site data is stored on a json file that contains all pw accounts
- Password are encrypted and the key is not written anywhere:
- the key is generated from the main PW password
- of course if you know the main PW password or the key, you can access to all the other stored passwords
- "other" field is meant for other kind of private data on a site account, and it can be accessed onlt throught main PW password. However strings are not yet encrypted in the json document, so for now is not safe to save other passwords or private codes on that field

## License
This project is released under the GNU General Public License.


## TODO
- [ ] pw change_password (cfr change_pw_comm.py)
- [ ] also encrypt all "other" section
- [ ] if the user wants to move to another password manager then he needs a file where all is saved and legible, maybe a csv or yaml file with all decrypted infos (some functions for csv are already implemented)
