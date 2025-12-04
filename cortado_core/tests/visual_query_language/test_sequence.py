import unittest
from cortado_core.utils.split_graph import (
    SequenceGroup,
    ParallelGroup,
    LeafGroup,
    StartGroup,
    EndGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class SimpleSequenceTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
            )
        )

    def test_exact_match(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
        )

        self.assertTrue(self.query.match(variant))

    def test_with_prefix(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertTrue(self.query.match(variant))

    def test_with_suffix(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y"]),
            ]
        )

        self.assertTrue(self.query.match(variant))

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

        self.assertTrue(self.query.match(variant))

    def test_non_matching(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["c"])]
        )

        self.assertFalse(self.query.match(variant))

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

        self.assertTrue(self.query.match(variant))

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

        self.assertFalse(self.query.match(variant))

    def wrongOrder(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["b"]), LeafGroup(lst=["a"])]
        )

        self.assertFalse(self.query.match(variant))

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

        self.assertFalse(self.query.match(variant))

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

        self.assertFalse(self.query.match(variant))


class PrefixSuffixTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
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
        self.assertTrue(self.query.match(variant))

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
        self.assertTrue(self.query.match(variant))

    def test_complete(self):
        query = create_query_instance(
            SequenceGroup(
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
        self.assertFalse(query.match(variant))


class MixedSequenceParallelTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["b"]),
                            SequenceGroup(
                                lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]
                            ),
                        ]
                    ),
                    LeafGroup(lst=["e"]),
                ],
            )
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

        activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        self.assertTrue(self.query.match(variant))
