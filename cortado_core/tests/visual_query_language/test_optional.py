import unittest

from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    OptionalGroup,
)
from cortado_core.visual_query_language.query import create_query_instance


class SimpleOptionalTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_one_element(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(lst=[LeafGroup(lst=["b"])]),
                    LeafGroup(lst=["c"]),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["c"])])

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )

        self.assertFalse(query.match(variant))

    def test_grouped(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(
                        lst=[
                            SequenceGroup(
                                lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
                            )
                        ]
                    ),
                    LeafGroup(lst=["d"]),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["d"])])

        self.assertTrue(query.match(variant))

        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"]), LeafGroup(lst=["d"])]
        )

        self.assertFalse(query.match(variant))

    def test_optional_parallel(self):
        query = create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(
                        lst=[
                            ParallelGroup(
                                lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
                            )
                        ]
                    ),
                    LeafGroup(lst=["d"]),
                ]
            )
        )

        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )

        self.assertFalse(query.match(variant))

        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["d"])])

        self.assertTrue(query.match(variant))

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

        self.assertTrue(query.match(variant))

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

        self.assertFalse(query.match(variant))
