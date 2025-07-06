"""
List all sites in the database
"""

from .data.strings import PW_LIST_COMM_NAME
from .data.utils import add_one_to_counter
from .pw_class import find_full_site_names


def list_comm(site_query: str, raw: bool) -> None:
    find_full_site_names(site_query, show_print=True, raw_print=raw)

    # +1 to usage counter
    add_one_to_counter(PW_LIST_COMM_NAME)
