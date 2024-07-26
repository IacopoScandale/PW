help_message = """
Pw copy to clipboard

Usage: pw <site_query>

Output: copies password linked to selected account to the clipboard
"""

from pw_class import copy_pw_from_json
from data_tmp.utils import help_and_error
import os, sys

help_and_error(help_message, sys.argv, 1)

# change directory to main project directory
os.chdir(os.path.dirname(sys.argv[0]))

site_query = sys.argv[1]
copy_pw_from_json(site_query)