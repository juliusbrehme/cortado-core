import unittest

from cortado_core.utils.split_graph import (
    SequenceGroup,
    LeafGroup,
    ParallelGroup,
    AnythingGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class SimpleAnythingTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[LeafGroup(lst=["a"]), AnythingGroup(), LeafGroup(lst=["b"])]
            )
        )

    def test_nothing_in_between(self):
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])])

        self.assertFalse(self.query.match(variant))

    def test_single_element_in_between(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["b"])]
        )

        self.assertTrue(self.query.match(variant))

    def test_multiple_elements_in_between(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertTrue(self.query.match(variant))

    def test_parallel_elements_in_between(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertTrue(self.query.match(variant))

    def test_non_matching(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["c"])]
        )

        self.assertFalse(self.query.match(variant))


class SpecialAnythingTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    def test_double_use(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["b"])]
        )

        self.assertFalse(query.match(variant))

    def test_two_anythings(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                    AnythingGroup(),
                    LeafGroup(lst=["c"]),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertFalse(query.match(variant))
