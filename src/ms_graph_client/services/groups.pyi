import enum
import typing
from ms_graph_client.graph_api_config import GraphAPIConfig as GraphAPIConfig
from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE as GraphAPICRUDBASE
from typing import Any, Optional

class Groups(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig) -> None: ...
    class GroupType(enum.Enum):
        SECURITY: str
        Microsoft365: str
    def is_group_assigned_to_app(self, app_service_principal_id: str, group_id: str) -> bool: ...
    def get_by_name(self, group_name: str) -> Any: ...
    def get_by_object_id(self, group_id: str) -> Any: ...
    def exists_by_name(self, group_name: str) -> bool: ...
    def delete(self, group_id: str, group_name: str, with_stabilization: bool) -> None: ...
    def update(self,
               group_id: str,
               group_name: Optional[str] = None ,
               group_description: Optional[str] = None
               ) -> None: ...
    def list_owners(self, group_id: str) -> list[Any]: ...
    def add_owner(self, group_id: str, user_obj_id: str) -> None: ...
    def remove_owner(self, group_id: str, user_obj_id: str) -> None: ...
    def _stabilize_group_existence(self, group_name: str, should_exist: bool) -> None: ...
    def create(self, group_name: str, group_description: str, group_type: GroupType, owners: list[str], with_stabilization: bool) -> str: ...
    def list_group_members(self, group_id: str, recursive:bool =True) -> list[Any]: ...
    def is_member_of_group(self, group_id: str, object_id: str) -> bool: ...
    def _stabilize_member_in_group_existence(self, group_id: str, object_id: str, should_exist: bool) -> None: ...
    def add_member(self, group_id: str, object_id: str, with_stabilization: bool) -> None: ...
    def _chunk_list(self, my_list: list[Any], size: int) -> typing.Iterator[Any]: ...
    def add_members(self, group_id: str, object_ids: list[str]) -> None: ...
    def remove_member(self, group_id: str, object_id: str, with_stabilization: bool) -> None: ...
