"""
Find a site from a site query and choose an account to remove
"""

from .data.strings import PW_REMOVE_COMM_NAME
from .data.utils import add_one_to_counter, input_pw_password
from .pw_class import PW, get_pw_obj_from_site_query


def remove_comm(site_query: str) -> None:
    pw_obj: PW = get_pw_obj_from_site_query(site_query)
    _ = input_pw_password()
    pw_obj.remove_from_database()

    # +1 to usage counter
    add_one_to_counter(PW_REMOVE_COMM_NAME)
