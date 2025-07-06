# PW
## CLI Password Manager

<!-- Badges -->
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Platform](https://img.shields.io/badge/platform-Linux,%20Windows,%20macOS-green) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)


**pw** is a command-line tool to securely store, copy and manage site account passwords.


## Table of Contents
- [Commands](#commands)
- [Examples](#examples)
  - [Add](#add)
  - [Info](#info)
  - [All Info](#all-info)
  - [Copy](#copy)
  - [List](#list)
  - [Edit](#edit)
  - [Remove](#remove)
- [Download](#download)
  - [Base Env (Easier)](#base-env-easier)
  - [Virtual Env (Recommended)](#virtual-env-recommended)
    - [Dependencies](#1-dependencies)
      - [uv](#uv)
      - [pip](#pip)
    - [pw bin file](#2-pw-bin-file)
      - [Linux and macOS](#linux-and-macos)
      - [Windows](#windows)
- [Security Notes](#security-notes)


# Commands
Command template:

```sh
pw [command] [options]
```
To show command usages:
```sh
pw

Commands:              Times Used:
——————————————————————————————————————
   1. pw                        41
   2. add                       34
   3. info                       5
   4. all_info                  27
   5. copy                      32
   6. list                      65
   7. edit                      44
   8. remove                     8
——————————————————————————————————————
      Total:                   256
```

| [command]      | Description |
|-------------|------------|
| `add`       | Add a new account to the database |
| `info`      | Show information related to a specific account (search by site query) |
| `all_info`  | Print all information related to a specific account (requires PW password) |
| `copy`      | Copy the password of the selected account to the clipboard |
| `list`      | List all sites stored in the database (supports filtering by site query) |
| `edit`      | Find an account by site query and edit it |
| `remove`    | Find an account by site query and remove it |

## Examples

#### Add
Add a new account to the database
```sh
pw add
```

### Info
Show information related to a specific account (search by site query)
```sh
pw info git  # git -> github.com
```


### All Info
Print all information related to a specific account (requires PW password)
```sh
pw all_info ithub  # ithub -> github.com
```

### Copy
Copy the password of the selected account to the clipboard
```sh
pw copy hub
```

### List
List all sites stored in the database (supports filtering by site query)

```sh
pw list

  1. github.com
  2. example.it
  3. example.com
```
```sh
pw list exa

  1. example.it
  2. example.com
```
```sh
pw list --raw

github.com
example.it
example.com
```

### Edit
Find an account by site query and edit it
```sh
# edit email and password
pw edit git --email new@mail --change-pw

# edit everything (site, mail, username, password and other section)
pw edit git -s new_site -e new_mail -u new_username -p -o
```


### Remove
Find an account by site query and remove it
```sh
pw remove example.com
```



# Download
There are two different ways, choose one:
- [Base Env (Easier)](#base-env-easier)
- [Virtual Env (Recommended)](#virtual-env-recommended)

## Base Env (Easier)
You can install this package (if compatible with python version and other dependencies) in your main python installation with pip. Just open a shell in the main project and type:
```sh
pip install -e .  # -e for editable mode
```
Uninstall:
```sh
pip uninstall .
```

## Virtual Env (Recommended)

### 1. Dependencies
#### [uv](https://github.com/astral-sh/uv)
```sh
uv sync
```
or
```sh
# create virtual env
uv venv

# activate env
source .venv/bin/activate  # linux or mac
.venv\Scripts\activate  # windows

# install requirements
uv pip install -e .  # -e for editable mode
```
#### pip
```sh
# create virtual env
python -m venv .venv

# activate env
source .venv/bin/activate  # linux or mac
.venv\Scripts\activate  # windows

# install requirements
pip install -e .  # -e for editable mode
```

### 2. pw bin file
Once step 1. is done, the following bin file (the actual terminal command) will be created:
```sh
.venv/bin/pw  # linux or mac
.venv\Scripts\pw.exe  # windows
```
To have it ready-to-use in every shell you should have to copy it and paste in a directory on `PATH`. The following directories are suggested, depending on your os:

#### Linux and macOS
```sh
# current user
cp .venv/bin/pw ~/.local/bin/

# or system wide:
sudo cp .venv/bin/pw /usr/local/bin/
```

#### Windows
An advice is to create the linux-equivalent: `"%USERPROFILE%\.local\bin"` directory and then add it on user `PATH`.
```sh
# for current user:

# create folder
mkdir "%USERPROFILE%\.local\bin"

# add it to user path
# do it through windows settings to avoid problems...

# copy the .exe file into it
copy .venv\Scripts\ffpdf.exe "%USERPROFILE%\.local\bin\"
```
Otherwise you can copy the .exe file into some other folders that are already on `PATH`, as for example `"%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\"`.


# Security Notes
- All site data is stored on a json file that contains all pw accounts
- Password are encrypted and the key is not written anywhere:
- the key is generated from the main PW password
- of course if you know the main PW password or the key, you can access to all the other stored passwords
- "other" field is meant for other kind of private data on a site account, and it can be accessed onlt throught main PW password. However strings are not yet encrypted in the json document, so for now is not safe to save other passwords or private codes on that field
