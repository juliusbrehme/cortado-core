import unittest

from cortado_core.utils.split_graph import (
    SequenceGroup,
    ParallelGroup,
    LeafGroup,
    ChoiceGroup,
)
from cortado_core.visual_query_language.query import check_variant


class SimpleStackTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = SequenceGroup(
            lst=(
                LeafGroup(lst=("a",)),
                ChoiceGroup(lst=(LeafGroup(lst=("b",)), LeafGroup(lst=("c",)))),
                LeafGroup(lst=("d",)),
            )
        )

        self.activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    def test_choice1(self):
        variant = SequenceGroup(
            lst=(LeafGroup(lst=("a",)), LeafGroup(lst=("b",)), LeafGroup(lst=("d",)))
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_choice2(self):
        variant = SequenceGroup(
            lst=(LeafGroup(lst=("a",)), LeafGroup(lst=("c",)), LeafGroup(lst=("d",)))
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))

    def test_non_matching(self):
        variant = SequenceGroup(
            lst=(LeafGroup(lst=("a",)), LeafGroup(lst=("e",)), LeafGroup(lst=("d",)))
        )

        self.assertFalse(check_variant(variant, self.query, self.activities))

    def test_additional_elements(self):
        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("x",)),
                LeafGroup(lst=("a",)),
                LeafGroup(lst=("b",)),
                LeafGroup(lst=("d",)),
                LeafGroup(lst=("y",)),
            )
        )

        self.assertTrue(check_variant(variant, self.query, self.activities))
