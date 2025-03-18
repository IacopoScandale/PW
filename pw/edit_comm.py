from .data.utils import add_one_to_counter
from .data.strings import PW_EDIT_COMM_NAME
from .pw_class import get_pw_obj_from_site_query


def edit_comm(site_query: str, **kwargs) -> None:
  ...

  pw_obj = get_pw_obj_from_site_query(site_query)
  pw_obj.edit(**kwargs)

  add_one_to_counter(PW_EDIT_COMM_NAME)