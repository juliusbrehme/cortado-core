import unittest
from cortado_core.utils.split_graph import (
    SequenceGroup,
    ParallelGroup,
    LeafGroup,
    StartGroup,
    EndGroup,
)
from cortado_core.visual_query_language.query import check_variant


class SimpleSequenceTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
        )

        self.activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    def test_exact_match(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_with_prefix(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_with_suffix(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y"]),
            ]
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_within(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y"]),
            ]
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_non_matching(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["c"])]
        )

        self.assertFalse(check_variant(variant, self.query, self.activities))

    def test_repeating_match(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_repeating_non_matching(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertFalse(check_variant(variant, self.query, self.activities))

    def wrongOrder(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["b"]), LeafGroup(lst=["a"])]
        )

        self.assertFalse(check_variant(variant, self.query, self.activities))

    def test_parallel(self):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )

        self.assertFalse(check_variant(variant, self.query, self.activities))

    def test_mixed(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["x"]),
                    ]
                ),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertFalse(check_variant(variant, self.query, self.activities))


class PrefixSuffixTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["d"]), LeafGroup(lst=["e"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ],
        )

    def test_prefix(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["d"]), LeafGroup(lst=["e"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.assertTrue(check_variant(variant, self.query, activities))

    def test_suffix(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["d"]), LeafGroup(lst=["e"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.assertTrue(check_variant(variant, self.query, activities))

    def test_complete(self):
        query = SequenceGroup(
            lst=[
                StartGroup(),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["d"]), LeafGroup(lst=["e"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                EndGroup(),
            ],
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                ParallelGroup(lst=[LeafGroup(lst=["d"]), LeafGroup(lst=["e"])]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.assertFalse(check_variant(variant, query, activities))


class MixedSequenceParallelTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                    ]
                ),
                LeafGroup(lst=["e"]),
            ],
        )

    def test_matching(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                        LeafGroup(lst=["b"]),
                    ]
                ),
                LeafGroup(lst=["e"]),
            ]
        )

        print(self.query)
        print("=========")
        print(variant)

        activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.assertTrue(check_variant(variant, self.query, activities))
