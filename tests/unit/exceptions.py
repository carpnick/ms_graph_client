import ms_graph_client

def test_exceptions() -> None:
    try:
        ms_graph_client.TooManyMatchingGroupsError("")
    except Exception:
        pass