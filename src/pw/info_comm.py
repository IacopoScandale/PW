"""
Show site infos for a given site query
"""

from .data.strings import PW_INFO_COMM_NAME
from .data.utils import add_one_to_counter
from .pw_class import print_site_info_command


def info_comm(site_query: str) -> None:
    print_site_info_command(site_query, False)

    # +1 to usage counter
    add_one_to_counter(PW_INFO_COMM_NAME)
