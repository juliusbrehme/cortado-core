import unittest

from itertools import permutations
from cortado_core.utils.split_graph import (
    LeafGroup,
    SequenceGroup,
    ParallelGroup,
    FallthroughGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class NoOrderTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    FallthroughGroup(
                        lst=[
                            LeafGroup(lst=["b"]),
                            LeafGroup(lst=["c"]),
                            LeafGroup(lst=["d"]),
                        ]
                    ),
                    LeafGroup(lst=["e"]),
                ]
            )
        )

    def test_order_match(self):
        for permutation in permutations(["b", "c", "d"]):
            variant = SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LeafGroup(lst=[permutation[0]]),
                    LeafGroup(lst=[permutation[1]]),
                    LeafGroup(lst=[permutation[2]]),
                    LeafGroup(lst=["e"]),
                ]
            )

            self.assertTrue(self.query.match(variant))

    def test_missing_element(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["e"]),
            ]
        )

        self.assertFalse(self.query.match(variant))

    def test_parallel_matching(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                    ]
                ),
                LeafGroup(lst=["e"]),
            ]
        )

        self.assertTrue(self.query.match(variant))

    def test_extra_element(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["e"]),
            ]
        )

        self.assertFalse(self.query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["e"]),
                    ]
                ),
                LeafGroup(lst=["e"]),
            ]
        )

        self.assertFalse(self.query.match(variant))

    def test_parallel_and_sequence(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["d"])]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["e"]),
            ]
        )

        self.assertTrue(self.query.match(variant))
