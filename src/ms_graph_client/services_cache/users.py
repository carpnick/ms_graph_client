from typing import Any, Optional

from ms_graph_client.services.users import Users as UsersCrud
import cachetools.func


class Users:
    def __init__(self, crud_client: UsersCrud):
        self._crud_client = crud_client

    @cachetools.func.ttl_cache(ttl=600)
    def get_user(self, upn: str, select_properties: Optional[frozenset[str]] = None) -> Any:
        my_list = None
        if select_properties is not None:
            my_list = list(select_properties)
        res = self._crud_client.get_user(upn=upn, select_properties=my_list)
        return res

    @cachetools.func.ttl_cache(ttl=600)
    def get_manager(self, upn: str) -> Any:
        res = self._crud_client.get_manager(upn=upn)
        return res
