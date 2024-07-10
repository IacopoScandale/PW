help_message = """
Pw copy to clipboard

Usage: pw <site_query>

Output: copies password linked to selected account to the clipboard
"""

from pw_class import copy_pw_from_json
from Data.constants import help_and_error
import sys

help_and_error(help_message, sys.argv, 1)

site_query = sys.argv[1]
copy_pw_from_json(site_query)