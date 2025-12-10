import pytest

from cortado_core.utils.split_graph import (
    SequenceGroup,
    LeafGroup,
    StartGroup,
    EndGroup,
)
from cortado_core.visual_query_language.query import create_query_instance
from cortado_core.tests.visual_query_language.query_type_fixture import query_type


class TestStart:
    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    StartGroup(),
                    LeafGroup(lst=["a"]),
                ]
            ),
            query_type=query_type,
        )

    def test_start(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        assert query.match(variant)

    def test_not_start(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
            ]
        )

        assert not query.match(variant)


class TestEnd:
    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    EndGroup(),
                ]
            ),
            query_type=query_type,
        )

    def test_end(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
            ]
        )

        assert query.match(variant)

    def test_not_end(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        assert not query.match(variant)


class TestStartEnd:
    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    StartGroup(),
                    LeafGroup(lst=["a"]),
                    EndGroup(),
                ]
            ),
            query_type=query_type,
        )

    def test_start_end(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
            ]
        )

        assert query.match(variant)

    def test_only_start(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        assert not query.match(variant)

    def test_only_end(self, query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
            ]
        )

        assert not query.match(variant)
