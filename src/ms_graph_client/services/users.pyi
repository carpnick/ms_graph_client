from ms_graph_client.graph_api_config import GraphAPIConfig as GraphAPIConfig
from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE as GraphAPICRUDBASE
from typing import Any

class Users(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig) -> None: ...
    def get_user(self, upn: str, select_properties:list[str] | None = None) -> Any:
        if select_properties is None:
            select_properties = []
        ...
    def get_manager(self,upn: str) -> Any: ...
