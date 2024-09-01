# PW

> package name: *pw*

Terminal site account password manager


# Download
Recommended install is by executing install files respectively .bat for windows and ??? for linux. 

This will install this package and dependencies in a virtual environment. Then all commands will be put in Commands folder that will automaticly added to path variable. In this way commands will always loaded on terminal. All this is done in the scrypt `post_install.py`. 

## Windows
Just double click on `setup.bat` file. If you want to uninstall just double click on `uninstall.bat` file. Easy peasy.

## Linux
Navigate into main project folder and execute this command: `./setup.sh` for installing pw commands. sudo powers are required for installation.

For undo installation just run `./uninstall.sh`. Then you can simply remove the folder. NB: passwords would not be removed, but they will remain encrypted with the old PW password.


# Commands:
|command|description|
|-|-|
|`pw`|prints PW project info and command names|
|`pw.add`|adds pw to database|
|`pw.info`|gets few info on pw|
|`pw.all_info`|gets all pw info (requires PW password)|
|`pw.copy`|copies pw to the clipboard|
 

Type `command_name -h` or `command_name --help` for more info
