import unittest

from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    OptionalGroup,
)
from cortado_core.visual_query_language.query import check_variant


class SimpleOptionalTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    def test_one_element(self):
        query = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                OptionalGroup(lst=[LeafGroup(lst=["b"])]),
                LeafGroup(lst=["c"]),
            ]
        )

        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
        )

        self.assertTrue(check_variant(variant, query, self.activities))

        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["c"])])

        self.assertTrue(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertFalse(check_variant(variant, query, self.activities))

    def test_grouped(self):
        query = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                OptionalGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])])
                    ]
                ),
                LeafGroup(lst=["d"]),
            ]
        )

        varaint = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )

        self.assertTrue(check_variant(varaint, query, self.activities))

        varaint = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["d"])])

        self.assertTrue(check_variant(varaint, query, self.activities))

        varaint = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["d"])]
        )

        self.assertFalse(check_variant(varaint, query, self.activities))

    def test_optional_parallel(self):
        query = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                OptionalGroup(
                    lst=[
                        ParallelGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])])
                    ]
                ),
                LeafGroup(lst=["d"]),
            ]
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )

        self.assertFalse(check_variant(variant, query, self.activities))

        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["d"])])

        self.assertTrue(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                ),
                LeafGroup(lst=["d"]),
            ]
        )

        self.assertTrue(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["e"]),
                    ]
                ),
                LeafGroup(lst=["d"]),
            ]
        )

        self.assertFalse(check_variant(variant, query, self.activities))
