"""
AI generated tests include:
- TestOptionalSingleElement: Tests optional single activities. Verifies element can be present or absent
- TestOptionalSequence: Tests optional sequences containing multiple elements. Verifies entire sequence is optional
- TestOptionalParallel: Tests optional parallel groups. Handles optional concurrent execution
- TestOptionalNested: Tests optionals nested inside other optionals. Verifies multiple levels of optionality
- TestOptionalInSequence: Tests optional elements within sequences. Various positions and combinations
- TestMultipleOptionals: Tests multiple distinct optionals in sequence. All combinations of present/absent
- TestOptionalWithLoop: Tests optional groups containing loops. Verifies loop bounds work inside optional
- TestOptionalInParallel: Tests optionals inside parallel groups. Concurrent execution with optionality
- TestOptionalWithChoice: Tests optional containing choice groups. Verifies choice works when optional is present
- TestOptionalComplexContent: Tests optional with deeply nested structures. Sequences, parallels, and choices combined
- TestOptionalAtStart: Tests optional at the beginning of sequence
- TestOptionalAtEnd: Tests optional at the end of sequence
- TestOptionalChain: Tests multiple consecutive optionals. All combinations of which are present
- TestOptionalLoopContent: Tests loop containing optional elements. Verifies optionality works per iteration
- TestOptionalParallelBranch: Tests optional branches in parallel. One or both branches can be optional
"""

import pytest
from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    OptionalGroup,
    LoopGroup,
    ChoiceGroup,
)
from cortado_core.visual_query_language.query import create_query_instance
from cortado_core.tests.visual_query_language.query_type_fixture import query_type


class TestOptionalSingleElement:
    """Test optional single activities in basic sequences"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(lst=[LeafGroup(lst=["b"])]),
                    LeafGroup(lst=["c"]),
                ]
            ),
            query_type=query_type,
        )

    def test_optional_present(self, query):
        """a b c - optional element is present"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert query.match(variant)

    def test_optional_absent(self, query):
        """a c - optional element is absent"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["c"])])
        assert query.match(variant)

    def test_optional_repeated(self, query):
        """a b b c - optional element appears twice (too many)"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert not query.match(variant)

    def test_optional_wrong_element(self, query):
        """a x c - wrong element instead of optional"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalSequence:
    """Test optional containing sequences"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    OptionalGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    LeafGroup(lst=["b"]),
                                    LeafGroup(lst=["c"]),
                                ]
                            )
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_sequence_present_complete(self, query):
        """start a b c end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_sequence_absent(self, query):
        """start end"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["start"]), LeafGroup(lst=["end"])])
        assert query.match(variant)

    def test_sequence_partial(self, query):
        """start a b end - incomplete optional sequence"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)

    def test_sequence_extra_element(self, query):
        """start a b c x end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalParallel:
    """Test optional containing parallel groups"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    OptionalGroup(
                        lst=[
                            ParallelGroup(
                                lst=[
                                    LeafGroup(lst=["x"]),
                                    LeafGroup(lst=["y"]),
                                ]
                            )
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_parallel_present_correct_order1(self, query):
        """start x y end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["x"]),
                        LeafGroup(lst=["y"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_parallel_present_correct_order2(self, query):
        """start y x end - parallel order doesn't matter"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["y"]),
                        LeafGroup(lst=["x"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_parallel_absent(self, query):
        """start end"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["start"]), LeafGroup(lst=["end"])])
        assert query.match(variant)

    def test_parallel_partial(self, query):
        """start x end - only one parallel element"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)

    def test_parallel_wrong_elements(self, query):
        """start a b end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalNested:
    """Test optionals nested inside other optionals"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["b"]),
                                    OptionalGroup(lst=[LeafGroup(lst=["c"])]),
                                    LeafGroup(lst=["d"]),
                                ]
                            )
                        ]
                    ),
                    LeafGroup(lst=["e"]),
                ]
            ),
            query_type=query_type,
        )

    def test_both_optionals_present(self, query):
        """a b c d e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_outer_optional_absent(self, query):
        """a e"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["e"])])
        assert query.match(variant)

    def test_inner_optional_absent(self, query):
        """a b d e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_both_optionals_absent(self, query):
        """a d e - inner optional absent, but outer still present"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)


class TestOptionalInSequence:
    """Test optional elements at various positions in sequences"""

    @pytest.fixture
    def query_middle(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(lst=[LeafGroup(lst=["b"])]),
                    LeafGroup(lst=["c"]),
                ]
            ),
            query_type=query_type,
        )

    def test_middle_optional_present(self, query_middle):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert query_middle.match(variant)

    def test_middle_optional_absent(self, query_middle):
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["c"])])
        assert query_middle.match(variant)

    @pytest.fixture
    def query_start(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    OptionalGroup(lst=[LeafGroup(lst=["a"])]),
                    LeafGroup(lst=["b"]),
                    LeafGroup(lst=["c"]),
                ]
            ),
            query_type=query_type,
        )

    def test_start_optional_present(self, query_start):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert query_start.match(variant)

    def test_start_optional_absent(self, query_start):
        variant = SequenceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])])
        assert query_start.match(variant)

    @pytest.fixture
    def query_end(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    LeafGroup(lst=["b"]),
                    OptionalGroup(lst=[LeafGroup(lst=["c"])]),
                ]
            ),
            query_type=query_type,
        )

    def test_end_optional_present(self, query_end):
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert query_end.match(variant)

    def test_end_optional_absent(self, query_end):
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])])
        assert query_end.match(variant)


class TestMultipleOptionals:
    """Test multiple optionals in sequence with all combinations"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    OptionalGroup(lst=[LeafGroup(lst=["b"])]),
                    OptionalGroup(lst=[LeafGroup(lst=["c"])]),
                    OptionalGroup(lst=[LeafGroup(lst=["d"])]),
                    LeafGroup(lst=["e"]),
                ]
            ),
            query_type=query_type,
        )

    def test_all_optionals_present(self, query):
        """a b c d e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_all_optionals_absent(self, query):
        """a e"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["e"])])
        assert query.match(variant)

    def test_first_optional_only(self, query):
        """a b e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_middle_optional_only(self, query):
        """a c e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_last_optional_only(self, query):
        """a d e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_first_and_last_optionals(self, query):
        """a b d e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)

    def test_first_and_middle_optionals(self, query):
        """a b c e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert query.match(variant)


class TestOptionalWithLoop:
    """Test optional groups containing loops"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    OptionalGroup(
                        lst=[
                            LoopGroup(
                                lst=[LeafGroup(lst=["x"])],
                                min_count=2,
                                max_count=3,
                            )
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_optional_loop_absent(self, query):
        """start end"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["start"]), LeafGroup(lst=["end"])])
        assert query.match(variant)

    def test_optional_loop_min(self, query):
        """start x x end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_optional_loop_max(self, query):
        """start x x x end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_optional_loop_too_few(self, query):
        """start x end - only 1 x, needs at least 2"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)

    def test_optional_loop_too_many(self, query):
        """start x x x x end - 4 x's, max is 3"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalInParallel:
    """Test optionals inside parallel groups"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    ParallelGroup(
                        lst=[
                            OptionalGroup(lst=[LeafGroup(lst=["a"])]),
                            LeafGroup(lst=["b"]),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_optional_in_parallel_present(self, query):
        """start || (a b) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_optional_in_parallel_absent(self, query):
        """start || (b) || end - only b, a is optional"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(lst=[LeafGroup(lst=["b"])]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_optional_in_parallel_wrong_element(self, query):
        """start || (c b) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["b"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalWithChoice:
    """Test optional containing choice groups"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    OptionalGroup(
                        lst=[
                            ChoiceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    LeafGroup(lst=["b"]),
                                ]
                            )
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_optional_choice_absent(self, query):
        """start end"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["start"]), LeafGroup(lst=["end"])])
        assert query.match(variant)

    def test_optional_choice_first_option(self, query):
        """start a end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_optional_choice_second_option(self, query):
        """start b end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_optional_choice_both_present(self, query):
        """start a b end - both options present"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)

    def test_optional_choice_wrong_element(self, query):
        """start c end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalComplexContent:
    """Test optional with deeply nested structures"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    OptionalGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    ParallelGroup(
                                        lst=[
                                            LeafGroup(lst=["b"]),
                                            ChoiceGroup(
                                                lst=[
                                                    LeafGroup(lst=["c"]),
                                                    LeafGroup(lst=["d"]),
                                                ]
                                            ),
                                        ]
                                    ),
                                    LeafGroup(lst=["e"]),
                                ]
                            )
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_complex_optional_absent(self, query):
        """start end"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["start"]), LeafGroup(lst=["end"])])
        assert query.match(variant)

    def test_complex_optional_present_with_c(self, query):
        """start a || (b c) || e end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                ),
                LeafGroup(lst=["e"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_complex_optional_present_with_d(self, query):
        """start a || (b d) || e end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["d"]),
                    ]
                ),
                LeafGroup(lst=["e"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_complex_optional_partial(self, query):
        """start a b c end - missing e before end"""
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


class TestOptionalChain:
    """Test chains of optional elements with various presence patterns"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["x"]),
                    OptionalGroup(lst=[LeafGroup(lst=["a"])]),
                    OptionalGroup(lst=[LeafGroup(lst=["b"])]),
                    OptionalGroup(lst=[LeafGroup(lst=["c"])]),
                    OptionalGroup(lst=[LeafGroup(lst=["d"])]),
                    LeafGroup(lst=["y"]),
                ]
            ),
            query_type=query_type,
        )

    def test_none_present(self, query):
        """x y"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])])
        assert query.match(variant)

    def test_alternating_present(self, query):
        """x a c y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y"]),
            ]
        )
        assert query.match(variant)

    def test_all_but_first(self, query):
        """x b c d y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["y"]),
            ]
        )
        assert query.match(variant)

    def test_all_but_last(self, query):
        """x a b c y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y"]),
            ]
        )
        assert query.match(variant)

    def test_alternating_all_odd(self, query):
        """x a c y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y"]),
            ]
        )
        assert query.match(variant)


class TestOptionalLoopContent:
    """Test loops containing optional elements"""

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
                                    OptionalGroup(lst=[LeafGroup(lst=["b"])]),
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

    def test_loop_with_optional_min_all_present(self, query):
        """start a b a b end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_loop_with_optional_min_all_absent(self, query):
        """start a a end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_loop_with_optional_min_mixed(self, query):
        """start a b a end - first has b, second doesn't"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_loop_with_optional_max_all_present(self, query):
        """start a b a b a b end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_loop_with_optional_max_all_absent(self, query):
        """start a a a end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)


class TestOptionalParallelBranch:
    """Test optional branches in parallel groups"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    ParallelGroup(
                        lst=[
                            OptionalGroup(
                                lst=[
                                    SequenceGroup(
                                        lst=[
                                            LeafGroup(lst=["a"]),
                                            LeafGroup(lst=["b"]),
                                        ]
                                    )
                                ]
                            ),
                            LeafGroup(lst=["x"]),
                            OptionalGroup(lst=[LeafGroup(lst=["y"])]),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_both_optionals_present(self, query):
        """start || (a b x y) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        LeafGroup(lst=["x"]),
                        LeafGroup(lst=["y"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_first_optional_absent(self, query):
        """start || (x y) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["x"]),
                        LeafGroup(lst=["y"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_second_optional_absent(self, query):
        """start || (a b x) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        LeafGroup(lst=["x"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_both_optionals_absent(self, query):
        """start || (x) || end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"])]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_required_parallel_absent(self, query):
        """start || (a b y) || end - missing required x"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        LeafGroup(lst=["y"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)


class TestOptionalWithMultipleElements:
    """Test optionals containing multiple distinct elements"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    OptionalGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    LeafGroup(lst=["b"]),
                                ]
                            )
                        ]
                    ),
                    OptionalGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["c"]),
                                    LeafGroup(lst=["d"]),
                                ]
                            )
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_both_optional_sequences_present(self, query):
        """start a b c d end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_first_optional_sequence_only(self, query):
        """start a b end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_second_optional_sequence_only(self, query):
        """start c d end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query.match(variant)

    def test_no_optional_sequences(self, query):
        """start end"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["start"]), LeafGroup(lst=["end"])])
        assert query.match(variant)

    def test_first_optional_partial(self, query):
        """start a end - incomplete first optional"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not query.match(variant)
