import unittest

from cortado_core.utils.split_graph import (
    SequenceGroup,
    LeafGroup,
    StartGroup,
    EndGroup,
)
from cortado_core.visual_query_language.query import check_variant


class StartEndTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.activities = [chr(i) for i in range(ord("a"), ord("z") + 1)]

    def test_start(self):
        query = SequenceGroup(
            lst=(
                StartGroup(),
                LeafGroup(
                    lst=("a",),
                ),
            )
        )

        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("a",)),
                LeafGroup(lst=("b",)),
            )
        )

        self.assertTrue(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("b",)),
                LeafGroup(lst=("a",)),
            )
        )

        self.assertFalse(check_variant(variant, query, self.activities))

    def test_end(self):
        query = SequenceGroup(
            lst=(
                LeafGroup(lst=("a",)),
                EndGroup(),
            )
        )

        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("a",)),
                LeafGroup(lst=("b",)),
            )
        )

        self.assertFalse(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("b",)),
                LeafGroup(lst=("a",)),
            )
        )

        self.assertTrue(check_variant(variant, query, self.activities))

    def test_start_end(self):
        query = SequenceGroup(
            lst=(
                StartGroup(),
                LeafGroup(lst=("a",)),
                EndGroup(),
            )
        )

        variant = SequenceGroup(lst=(LeafGroup(lst=("a",)),))

        self.assertTrue(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("b",)),
                LeafGroup(lst=("a",)),
            )
        )

        self.assertFalse(check_variant(variant, query, self.activities))

        variant = SequenceGroup(
            lst=(
                LeafGroup(lst=("a",)),
                LeafGroup(lst=("b",)),
            )
        )

        self.assertFalse(check_variant(variant, query, self.activities))
