import ms_graph_client as d


def test_parameters() -> None:
    s = d.graph_api_config.GraphAPIConfig(client_id="1", client_secret="2", tenant_id="3", api_url="4")
    assert s.tenant_id == "3"
    assert s.client_id == "1"
    assert s.api_url == "4"
    assert s.client_secret == "2"
