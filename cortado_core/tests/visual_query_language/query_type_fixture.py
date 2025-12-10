import pytest
from cortado_core.visual_query_language.query import QueryType


@pytest.fixture(params=[QueryType.DFS])
def query_type(request):
    return request.param
