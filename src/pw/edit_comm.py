"""
Change site infos
"""

from rich import print

from .data.strings import PW_EDIT_COMM_NAME
from .data.utils import add_one_to_counter
from .pw_class import PW, get_pw_obj_from_site_query


def edit_comm(site_query: str, **kwargs) -> None:
    pw_obj: PW = get_pw_obj_from_site_query(site_query)

    print(pw_obj.print_site())

    pw_obj.edit(**kwargs)

    # +1 to usage counter
    add_one_to_counter(PW_EDIT_COMM_NAME)
