"""
Copy site password to the clipboard
"""

from .data.strings import PW_COPY_COMM_NAME
from .data.utils import add_one_to_counter
from .pw_class import copy_pw_from_json


def copy_comm(site_query: str, keep: int = 15) -> None:
    copy_pw_from_json(site_query, keep)

    # +1 to usage counter
    add_one_to_counter(PW_COPY_COMM_NAME)
