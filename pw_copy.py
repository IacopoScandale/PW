help_message = """
Pw copy to clipboard

Usage: pw <site_query>

Output: copies password linked to selected account to the clipboard
"""

from pw_class import PW, find_full_site_names, create_objects_from_json
from Data.constants import help_and_error
import os, sys

help_and_error(help_message, sys.argv, 1)

site_query = sys.argv[1]
sites = find_full_site_names(site_query)

# case no sites found
if sites == [""]:
  sys.exit()

# rapid case when site_query == site
if site_query in sites:
  site = site_query
  # TODO enumerate all obj pairs (username, email)?




# rapid case when there is only one site found in sites
elif len(sites) == 1:
  site = sites[0]
  ask = input(f"{site}?\n [Y,n]: ")
  if ask in "yYsS":
    # TODO
    pass

else:
  # enumerate all sites
  for i, site in enumerate(sites):
    print(f"{i+1}. {site}")

  # ask for index
  selected_idx = int(input("Select site number: ")) - 1
  site = sites[selected_idx] 
  # TODO 
  






# copy pw
os.system(f'echo {pw}| clip')