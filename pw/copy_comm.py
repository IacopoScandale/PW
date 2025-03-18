from .data.utils import add_one_to_counter
from .data.strings import PW_COPY_COMM_NAME
from .pw_class import copy_pw_from_json


def copy_comm(site_query: str) -> None:
  copy_pw_from_json(site_query)

  add_one_to_counter(PW_COPY_COMM_NAME)