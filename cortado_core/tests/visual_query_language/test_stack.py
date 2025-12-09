import unittest

from cortado_core.utils.split_graph import (
    SequenceGroup,
    ParallelGroup,
    LeafGroup,
    ChoiceGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class SimpleStackTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    ChoiceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]),
                    LeafGroup(lst=["d"]),
                ]
            )
        )

    def test_choice1(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["d"])]
        )

        self.assertTrue(self.query.match(variant))

    def test_choice2(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]
        )

        self.assertTrue(self.query.match(variant))

    def test_non_matching(self):
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["e"]), LeafGroup(lst=["d"])]
        )

        self.assertFalse(self.query.match(variant))

    def test_additional_elements(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["y"]),
            ]
        )

        self.assertTrue(self.query.match(variant))
