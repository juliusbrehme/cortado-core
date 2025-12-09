import unittest

from cortado_core.utils.split_graph import (
    SequenceGroup,
    LeafGroup,
    StartGroup,
    EndGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class StartEndTest(unittest.TestCase):
    def test_start(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    StartGroup(),
                    LeafGroup(lst=["a"]),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
            ]
        )

        self.assertFalse(query.match(variant))

    def test_end(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    EndGroup(),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertFalse(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
            ]
        )

        self.assertTrue(query.match(variant))

    def test_start_end(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    StartGroup(),
                    LeafGroup(lst=["a"]),
                    EndGroup(),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
            ]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
            ]
        )

        self.assertFalse(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertFalse(query.match(variant))
