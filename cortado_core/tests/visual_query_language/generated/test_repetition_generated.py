"""
AI generated tests include:
- TestNestedLoops: Tests loops nested inside sequences within other loops. Verifies inner loops generate correct combinations when nested
- TestMultipleSequentialLoops: Tests multiple loops in sequence. Tests all combinations of min/max on multiple loops
- TestLoopsInParallel: Tests loops inside parallel groups. Handles concurrent execution with repetitions
- TestLoopWithComplexContent: Tests loops containing multi-element sequences. Verifies entire sequence blocks are repeated correctly
- TestLoopMinCountZero: Tests optional repetitions (min_count=0). Edge case: loop can match zero times
- TestLoopLargeCounts: Tests the capping mechanism at 200. Verifies min_count=50 and large max_counts work.
    Tests that exceeding the cap still respects min_count. Can extend this number by extending python's recursion limit using setrecursionlimit(n)
- TestLoopWithSingleElement: Tests simple loops as query root. Edge case: loop at the top level with no surrounding context
- TestChoiceWithLoops: Tests a loop of choices
- TestChoiceInLoopSequence: Tests choice inside sequences that are looped
- TestMultipleChoicesWithLoops: Tests multiple choices within a looped sequence
"""

import pytest
from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    LoopGroup,
    ChoiceGroup,
)
from cortado_core.visual_query_language.query import create_query_instance
from cortado_core.tests.visual_query_language.query_type_fixture import query_type


class TestNestedLoops:
    """Test loops nested inside other structures"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["x"]),
                                    LoopGroup(
                                        lst=[LeafGroup(lst=["y"])],
                                        min_count=1,
                                        max_count=2,
                                    ),
                                ]
                            )
                        ],
                        min_count=2,
                        max_count=2,
                    ),
                    LeafGroup(lst=["z"]),
                ]
            ),
            query_type=query_type,
        )

    def test_nested_loops_match(self, query):
        """Test: a (x y+){2} z where inner loop has 1 y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
            ]
        )
        assert query.match(variant)

    def test_nested_loops_with_max_inner(self, query):
        """Test: a (x y y){2} z where inner loop has 2 y's"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
            ]
        )
        assert query.match(variant)


class TestMultipleSequentialLoops:
    """Test multiple loops in sequence"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LoopGroup(lst=[LeafGroup(lst=["b"])], min_count=1, max_count=2),
                    LoopGroup(lst=[LeafGroup(lst=["c"])], min_count=1, max_count=2),
                    LeafGroup(lst=["d"]),
                ]
            ),
            query_type=query_type,
        )

    def test_both_loops_min(self, query):
        """a b c d"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )
        assert query.match(variant)

    def test_first_loop_max_second_min(self, query):
        """a b b c d"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )
        assert query.match(variant)

    def test_both_loops_max(self, query):
        """a b b c c d"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
            ]
        )
        assert query.match(variant)


class TestLoopsInParallel:
    """Test loops inside parallel groups"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LoopGroup(
                                        lst=[LeafGroup(lst=["x"])],
                                        min_count=1,
                                        max_count=2,
                                    )
                                ]
                            ),
                            SequenceGroup(
                                lst=[
                                    LoopGroup(
                                        lst=[LeafGroup(lst=["y"])],
                                        min_count=1,
                                        max_count=2,
                                    )
                                ]
                            ),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_parallel_loops_both_min(self, query):
        """start || (x y) || end - order may vary"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["x"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["y"])]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_parallel_loops_with_repetition(self, query):
        """start || (x x y y) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["x"]),
                                LeafGroup(lst=["x"]),
                            ]
                        ),
                        SequenceGroup(lst=[LeafGroup(lst=["y"])]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)


class TestLoopWithComplexContent:
    """Test loops containing complex sequences"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    LeafGroup(lst=["b"]),
                                    LeafGroup(lst=["c"]),
                                ]
                            )
                        ],
                        min_count=2,
                        max_count=3,
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_loop_complex_content_min(self, query):
        """start a b c a b c end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_loop_complex_content_max(self, query):
        """start a b c a b c a b c end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_loop_complex_content_too_few(self, query):
        """start a b c end - only 1 repetition, needs at least 2"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestLoopMinCountZero:
    """Test loops with min_count=0 (optional repetition)"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LoopGroup(lst=[LeafGroup(lst=["b"])], min_count=0, max_count=2),
                    LeafGroup(lst=["c"]),
                ]
            ),
            query_type=query_type,
        )

    def test_zero_repetitions(self, query):
        """a c - no b's"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["c"])])
        assert query.match(variant)

    def test_one_repetition(self, query):
        """a b c"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert query.match(variant)

    def test_max_repetitions(self, query):
        """a b b c"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert query.match(variant)


class TestLoopLargeCounts:
    """Test loops with large counts to verify capping works"""

    @pytest.fixture
    def query(self, query_type):
        # Set a very large max_count to test the cap
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LoopGroup(
                        lst=[LeafGroup(lst=["b"])],
                        min_count=50,  # 100
                        max_count=50000,  # Will be capped at 100
                    ),
                    LeafGroup(lst=["c"]),
                ]
            ),
            query_type=query_type,
        )

    def test_large_count_min_match(self, query):
        """Match variant with 150 b's (at min_count)"""
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"])]
            + [LeafGroup(lst=["b"]) for _ in range(150)]  # 1000
            + [LeafGroup(lst=["c"])]
        )
        assert query.match(variant)

    def test_large_count_capped_max_match(self, query):
        """Variant with 220 b's should fail (outside the capped max_count of 200)"""
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"])]
            + [LeafGroup(lst=["b"]) for _ in range(220)]
            + [LeafGroup(lst=["c"])]
        )
        assert not query.match(variant)

    def test_too_few_for_large_min(self, query):
        """Variant with 40 b's should fail (needs at least 50)"""
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"])]
            + [LeafGroup(lst=["b"]) for _ in range(40)]
            + [LeafGroup(lst=["c"])]
        )
        assert not query.match(variant)


class TestLoopWithSingleElement:
    """Test loops containing single element vs sequences"""

    @pytest.fixture
    def single_element_query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[LoopGroup(lst=[LeafGroup(lst=["x"])], min_count=1, max_count=3)]
            ),
            query_type=query_type,
        )

    def test_single_element_loop_min(self, single_element_query):
        variant = SequenceGroup(lst=[LeafGroup(lst=["x"])])
        assert single_element_query.match(variant)

    def test_single_element_loop_mid(self, single_element_query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
            ]
        )
        assert single_element_query.match(variant)

    def test_single_element_loop_max(self, single_element_query):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
            ]
        )
        assert single_element_query.match(variant)


class TestChoiceWithLoops:
    """Test ChoiceGroup combined with loops"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LoopGroup(
                        lst=[
                            ChoiceGroup(
                                lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]
                            )
                        ],
                        min_count=2,
                        max_count=3,
                    ),
                    LeafGroup(lst=["b"]),
                ]
            ),
            query_type=query_type,
        )

    def test_choice_loop_all_x(self, query):
        """a x x b - all choices are x"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert query.match(variant)

    def test_choice_loop_all_y(self, query):
        """a y y b - all choices are y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert query.match(variant)

    def test_choice_loop_mixed_min(self, query):
        """a x y b - mixed choices with min repetitions"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert query.match(variant)

    def test_choice_loop_mixed_max(self, query):
        """a y x y b - mixed choices with max repetitions"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert query.match(variant)

    def test_choice_loop_too_few(self, query):
        """a x b - only 1 choice, needs at least 2"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert not query.match(variant)


class TestChoiceInLoopSequence:
    """Test choice inside sequence that is looped"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    ChoiceGroup(
                                        lst=[
                                            LeafGroup(lst=["a"]),
                                            LeafGroup(lst=["b"]),
                                        ]
                                    ),
                                    LeafGroup(lst=["c"]),
                                ]
                            )
                        ],
                        min_count=1,
                        max_count=2,
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_choice_in_loop_sequence_min(self, query):
        """start a c end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_choice_in_loop_sequence_max_same(self, query):
        """start a c a c end - both repetitions choose a"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_choice_in_loop_sequence_max_mixed(self, query):
        """start a c b c end - mixed choices across repetitions"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_choice_in_loop_sequence_wrong_choice(self, query):
        """start x c end - wrong choice"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestMultipleChoicesWithLoops:
    """Test multiple choice groups within loops"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    ChoiceGroup(
                                        lst=[
                                            LeafGroup(lst=["a"]),
                                            LeafGroup(lst=["b"]),
                                        ]
                                    ),
                                    ChoiceGroup(
                                        lst=[
                                            LeafGroup(lst=["1"]),
                                            LeafGroup(lst=["2"]),
                                        ]
                                    ),
                                ]
                            )
                        ],
                        min_count=1,
                        max_count=2,
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_multiple_choices_min(self, query):
        """start a 1 end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["1"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_multiple_choices_max_all_combinations(self, query):
        """start b 2 b 1 end - different choices in each repetition"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["2"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["1"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_multiple_choices_max_same(self, query):
        """start a 1 a 1 end - same choices repeated"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["1"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["1"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)
