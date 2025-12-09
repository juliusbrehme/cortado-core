import unittest

from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    WildcardGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class SimpleWildcardTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[LeafGroup(lst=["a"]), WildcardGroup(), LeafGroup(lst=["b"])]
            )
        )

    def test_wildcard_matching(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["b"])]
        )

        self.assertTrue(self.query.match(variant))

        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["y"]), LeafGroup(lst=["b"])]
        )

        self.assertTrue(self.query.match(variant))

    def test_wildcard_with_multiple_elements(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertFalse(self.query.match(variant))

    def test_wildcard_parallel(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertFalse(self.query.match(variant))
