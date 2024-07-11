help_message = """
Usage: pw.info <site_query>
Usage: pw.info_pw <site_query>

Output: prints some infos linked to chosen site found from site query
"""

from Data.constants import help_and_error
from pw_class import find_full_site_names, print_all_pw
import os, sys


# argv[1] is given from commands.bat or commands.sh file: it is True or False and goes to `print_all_pw`
# argv[2] is the site query
help_and_error(help_message, sys.argv, 2)
# change directory to main project directory
os.chdir(os.path.dirname(sys.argv[0]))
# argv[1] print_pw
print_pw = sys.argv[1]
if print_pw == "True":
  print_pw = True
elif print_pw == "False":
  print_pw = False
# argv[2] site query
site_query = sys.argv[2]
sites = find_full_site_names(site_query)

# case no sites found
if sites == [""]:
  sys.exit()

# rapid case when site_query == site
if site_query in sites:
  site = site_query
  # print site accounts
  print_all_pw(site, print_pw)

# rapid case when there is only one site found in sites
elif len(sites) == 1:
  site = sites[0]
  ask = input(f"{site}?\n [Y,n]: ")
  if ask in "yYsS":
    # print site accounts
    print_all_pw(site, print_pw)

else:
  # enumerate all sites
  for i, site in enumerate(sites):
    print(f"{i+1}. {site}")

  # ask for index
  selected_idx = int(input("Select site number: ")) - 1
  site = sites[selected_idx] 
  # print site accounts
  print_all_pw(site, print_pw)