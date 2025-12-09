import unittest

from cortado_core.utils.split_graph import LeafGroup, ParallelGroup, SequenceGroup
from cortado_core.visual_query_language.query import create_query_instance


class SimpleParallelTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query = create_query_instance(
            SequenceGroup(
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
        )

    def test_exact_match(self):
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

        self.assertTrue(self.query.match(variant))

    def test_with_additional_branch(self):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )

        self.assertFalse(self.query.match(variant))

    def test_missing_branch(self):
        variant = SequenceGroup(
            lst=[ParallelGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])])]
        )

        self.assertFalse(self.query.match(variant))

    def test_different_order(self):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )

        self.assertTrue(self.query.match(variant))

    def test_in_sequence(self):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                ),
                LeafGroup(lst=["y"]),
            ]
        )

        self.assertTrue(self.query.match(variant))
