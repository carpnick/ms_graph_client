from typing import Any

from ms_graph_client.exceptions import UnableToFindUserError, UnableToFindManagerError
from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE
from ms_graph_client.graph_api_config import GraphAPIConfig
import requests


class Users(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig):
        super().__init__(config=config)

    def get_user(self, upn: str, select_properties: list[str] = None) -> Any:

        select_string = None
        if select_properties is not None:
            # $select=displayName,userPrincipalName,id,department
            select_string = "$select="
            for item in select_properties:
                select_string += item + ","
            select_string = select_string.strip(",")

        try:
            if select_string:
                # print(select_string)
                res = self._get(url_part="/users/" + upn + "?" + select_string)
            else:
                res = self._get(url_part="/users/" + upn)
            return res
        except Exception as e:
            if e.__cause__.__class__ == requests.exceptions.HTTPError:
                if e.__cause__.response.status_code == 404:
                    raise UnableToFindUserError(upn) from e
            # Default reraise
            raise

    def get_manager(self, upn: str) -> Any:
        try:
            res = self._get(url_part="/users/" + upn + "/manager")
            return res
        except Exception as e:
            if e.__cause__.__class__ == requests.exceptions.HTTPError:
                if e.__cause__.response.status_code == 404:
                    raise UnableToFindManagerError(upn) from e
            # Default reraise
            raise
