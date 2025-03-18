"""
Find a site from a site query and choose an account to remove
"""
from .data.utils import add_one_to_counter
from .data.strings import PW_REMOVE_COMM_NAME
from .pw_class import PW, get_pw_obj_from_site_query


def remove_comm(site_query: str) -> None:
  pw_obj: PW = get_pw_obj_from_site_query(site_query)
  pw_obj.remove_from_database()
  add_one_to_counter(PW_REMOVE_COMM_NAME)