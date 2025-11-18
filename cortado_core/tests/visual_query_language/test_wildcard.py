import unittest

from cortado_core.utils.split_graph import ParallelGroup, SequenceGroup, LeafGroup, WildcardGroup
from cortado_core.visual_query_language.query import check_variant


class SimpleWildcardTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            WildcardGroup(),
            LeafGroup(lst=["b"])
        ])

        self.activities = [chr(i) for i in range(ord("a"), ord("z")+1)]

    def test_wildcard_matching(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["x"]),
            LeafGroup(lst=["b"])
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))

        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["y"]),
            LeafGroup(lst=["b"])
        ])

        self.assertTrue(check_variant(variant, self.query, self.activities))

    
    def test_wildcard_with_multiple_elements(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            LeafGroup(lst=["x"]),
            LeafGroup(lst=["y"]),
            LeafGroup(lst=["b"])
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))


    def test_wildcard_parallel(self):
        variant = SequenceGroup(lst=[
            LeafGroup(lst=["a"]),
            ParallelGroup(lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"])
            ]),
            LeafGroup(lst=["b"])
        ])

        self.assertFalse(check_variant(variant, self.query, self.activities))
