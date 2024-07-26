@echo off

doskey pw_.add = D:\Documenti\GitHub\PW\venv\Scripts\python.exe D:\Documenti\GitHub\PW\pw_add.py  $*
doskey pw_.info = D:\Documenti\GitHub\PW\venv\Scripts\python.exe D:\Documenti\GitHub\PW\pw_site_info.py False $*
doskey pw_.all_info = D:\Documenti\GitHub\PW\venv\Scripts\python.exe D:\Documenti\GitHub\PW\pw_site_info.py True $*
doskey pw_.copy = D:\Documenti\GitHub\PW\venv\Scripts\python.exe D:\Documenti\GitHub\PW\pw_copy.py  $*
doskey pw_ = D:\Documenti\GitHub\PW\venv\Scripts\python.exe D:\Documenti\GitHub\PW\pw_help.py  $*
