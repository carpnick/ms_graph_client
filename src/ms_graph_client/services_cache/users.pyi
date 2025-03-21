from ms_graph_client.services.users import Users as UsersCrud
from typing import Any, Optional


class Users:
    _crud_client: UsersCrud
    def __init__(self, crud_client: UsersCrud) -> None: ...
    def get_user(self, upn: str, select_properties: Optional[frozenset[str]] = None ) -> Any: ...
    def get_manager(self,upn: str) -> Any: ...
