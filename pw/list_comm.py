from .data.utils import add_one_to_counter
from .data.strings import PW_LIST_COMM_NAME
from .pw_class import find_full_site_names

def list_comm(site_query: str) -> None:
  find_full_site_names(site_query, show_print=True)

  add_one_to_counter(PW_LIST_COMM_NAME)