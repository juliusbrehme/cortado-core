import unittest
from cortado_core.utils.split_graph import SequenceGroup, ParallelGroup, LeafGroup
from cortado_core.visual_query_language.query import check_variant


class SimpleSequenceTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"])
        ])

        self.activities = [chr(i) for i in range(ord("a"), ord("z")+1)]


    def test_exact_match(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"])
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))


    def test_with_prefix(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["x"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"])
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))

    
    def test_with_suffix(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"]),
            LeafGroup(lst=["y"])
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))


    def test_within(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["x"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"]),
            LeafGroup(lst=["y"])
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))


    def test_non_matching(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["x"]),
            LeafGroup(lst=["c"])
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))


    def test_repeating_match(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))
    

    def test_repeating_non_matching(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))


    def wrongOrder(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["c"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["a"])
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))


    def test_parallel(self):
        variant = ParallelGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["b"]),
            LeafGroup(lst=["c"])
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))


    def test_mixed(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            ParallelGroup(lst=[
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["x"]),
            ]),
            LeafGroup(lst=["c"])
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))