import unittest

from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    LoopGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class SimpleRepitionTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LoopGroup(lst=[LeafGroup(lst=["b"])], min_count=2, max_count=2),
                    LeafGroup(lst=["c"]),
                ]
            )
        )

    def test_match(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertTrue(self.query.match(variant))

    def test_too_few_repetitions(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
        )

        self.assertFalse(self.query.match(variant))

    def test_too_many_repetitions(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertFalse(self.query.match(variant))
