from typing import Any

from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE
from ms_graph_client.graph_api_config import GraphAPIConfig


class Users(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig):
        super().__init__(config=config)

    def get_user(self, upn: str) -> Any:
        "carpnick2@qkdw.onmicrosoft.com"
        res = self._get(url_part="/users/" + upn)
        return res
