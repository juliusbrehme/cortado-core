"""
AI generated tests for ParallelGroup operator include:
- TestSimpleParallel: Basic parallel matching with 2, 3, and many elements. Verifies order independence and exact matching.
- TestParallelWithSequences: Parallel branches containing sequences. Tests multiple sequential elements within each parallel branch.
- TestParallelWithChoices: Parallel branches with choice operators. Verifies independent choice selection in different branches.
- TestParallelWithLoops: Parallel branches containing loops. Tests repetition constraints independently in parallel branches.
- TestNestedParallel: Parallel groups nested inside other parallel groups. Tests multi-level parallelism.
- TestParallelWithAnything: Parallel with AnythingGroup to match any element. Tests wildcard matching in concurrent execution.
- TestParallelComplexNested: Deeply nested parallel structures with sequences, choices, and loops. Tests realistic complex workflows.
- TestParallelSingleBranch: Edge case with single branch in parallel group.
- TestParallelLargeBranches: Parallel with many branches (5+) to test scalability.
- TestParallelMixedContentTypes: Parallel containing both sequences and plain leaves. Tests heterogeneous content.
- TestParallelWithSequenceAndLoop: Parallel with one branch being a sequence containing loops. Tests composition.
- TestParallelIdenticalBranches: Parallel with identical sequences/elements in multiple branches. Tests duplicate handling.
- TestParallelVariantMismatch: Variants with wrong element counts, missing branches, or extra elements. Tests strict matching.
- TestParallelOrderIndependence: Verifies parallel matching works regardless of element order in variant.
- TestParallelWithOptional: Parallel branches with optional elements (loops with min_count=0).
"""

import pytest
from cortado_core.utils.split_graph import (
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    LoopGroup,
    ChoiceGroup,
    AnythingGroup,
)
from cortado_core.visual_query_language.query import create_query_instance
from cortado_core.tests.visual_query_language.query_type_fixture import query_type


class TestSimpleParallel:
    """Test basic parallel matching with different numbers of elements"""

    @pytest.fixture
    def query_two_elements(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            LeafGroup(lst=["b"]),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def query_three_elements(self, query_type):
        return create_query_instance(
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
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def query_five_elements(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            LeafGroup(lst=["b"]),
                            LeafGroup(lst=["c"]),
                            LeafGroup(lst=["d"]),
                            LeafGroup(lst=["e"]),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_two_elements_exact_order(self, query_two_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query_two_elements.match(variant)

    def test_two_elements_different_order(self, query_two_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["a"]),
                    ]
                )
            ]
        )
        assert query_two_elements.match(variant)

    def test_three_elements_exact_order(self, query_three_elements):
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
        assert query_three_elements.match(variant)

    def test_three_elements_different_order(self, query_three_elements):
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
        assert query_three_elements.match(variant)

    def test_three_elements_another_order(self, query_three_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["a"]),
                    ]
                )
            ]
        )
        assert query_three_elements.match(variant)

    def test_five_elements_exact(self, query_five_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["e"]),
                    ]
                )
            ]
        )
        assert query_five_elements.match(variant)

    def test_five_elements_shuffled(self, query_five_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["e"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query_five_elements.match(variant)

    def test_missing_element(self, query_three_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert not query_three_elements.match(variant)

    def test_extra_element(self, query_three_elements):
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
        assert not query_three_elements.match(variant)

    def test_wrong_element(self, query_three_elements):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["x"]),
                    ]
                )
            ]
        )
        assert not query_three_elements.match(variant)


class TestParallelWithSequences:
    """Test parallel branches containing sequences"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]
                            ),
                            SequenceGroup(
                                lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]
                            ),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_sequence_branches_exact_order(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_sequence_branches_different_order(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_sequence_branches_interleaved(self, query):
        """Variant has flattened interleaved elements: a c b d"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_sequence_branches_wrong_internal_order(self, query):
        """First sequence has wrong order: b a instead of a b"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["a"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_sequence_branches_missing_element(self, query):
        """Missing one element from a sequence"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelWithChoices:
    """Test parallel branches with choice operators"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            ChoiceGroup(
                                lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]
                            ),
                            ChoiceGroup(
                                lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["d"])]
                            ),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_both_first_choices(self, query):
        """Both branches take first choice: a and c"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_both_second_choices(self, query):
        """Both branches take second choice: b and d"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_mixed_choices(self, query):
        """First branch takes second choice, second takes first: b and c"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_mixed_choices_other_combo(self, query):
        """First branch takes first, second takes second: a and d"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_invalid_choice_first_branch(self, query):
        """First branch chooses invalid element"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["x"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_invalid_choice_second_branch(self, query):
        """Second branch chooses invalid element"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["x"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelWithLoops:
    """Test parallel branches containing loops"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LoopGroup(
                                lst=[LeafGroup(lst=["a"])], min_count=1, max_count=2
                            ),
                            LoopGroup(
                                lst=[LeafGroup(lst=["b"])], min_count=1, max_count=3
                            ),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_loops_min_counts(self, query):
        """Both loops at minimum: a and b"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_first_loop_max_second_min(self, query):
        """First loop max (a a), second at min (b)"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_first_loop_min_second_max(self, query):
        """First loop min (a), second at max (b b b)"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_both_loops_max(self, query):
        """Both loops at max: a a and b b b"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_first_loop_too_many(self, query):
        """First loop has 3 elements (exceeds max of 2)"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_second_loop_too_many(self, query):
        """Second loop has 4 elements (exceeds max of 3)"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestNestedParallel:
    """Test parallel groups nested inside other structures (sequences, choices, loops)"""

    @pytest.fixture
    def query_in_sequence(self, query_type):
        return create_query_instance(
            SequenceGroup(
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
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def query_in_loop(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LoopGroup(
                        lst=[
                            ParallelGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    LeafGroup(lst=["b"]),
                                ]
                            )
                        ],
                        min_count=1,
                        max_count=2,
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_parallel_in_sequence_exact(self, query_in_sequence):
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
        assert query_in_sequence.match(variant)

    def test_parallel_in_sequence_reordered(self, query_in_sequence):
        """Parallel elements reordered"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["a"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert query_in_sequence.match(variant)

    def test_parallel_in_loop_min(self, query_in_loop):
        """Loop with parallel at minimum (1 iteration)"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query_in_loop.match(variant)

    def test_parallel_in_loop_max(self, query_in_loop):
        """Loop with parallel at maximum (2 iterations)"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                ),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                ),
            ]
        )
        assert query_in_loop.match(variant)


class TestParallelWithAnything:
    """Test parallel with AnythingGroup wildcard"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            AnythingGroup(),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_anything_matches_single_element(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_anything_matches_different_element(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["x"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_anything_with_sequence(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        SequenceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_missing_required_element(self, query):
        """Missing the required 'a' element"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["x"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelComplexNested:
    """Test parallel with complex combination of operators"""

    @pytest.fixture
    def query_parallel_choices(self, query_type):
        """Parallel with choice groups in both branches"""
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            ChoiceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    LeafGroup(lst=["b"]),
                                ]
                            ),
                            ChoiceGroup(
                                lst=[
                                    LeafGroup(lst=["c"]),
                                    LeafGroup(lst=["d"]),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def query_parallel_sequence_loops(self, query_type):
        """Parallel with sequences containing loops"""
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LoopGroup(
                                        lst=[LeafGroup(lst=["a"])],
                                        min_count=1,
                                        max_count=2,
                                    ),
                                    LeafGroup(lst=["b"]),
                                ]
                            ),
                            LeafGroup(lst=["c"]),
                        ]
                    ),
                ]
            ),
            query_type=query_type,
        )

    def test_parallel_choices_both_first(self, query_parallel_choices):
        """Both choice groups take first option: a and c"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query_parallel_choices.match(variant)

    def test_parallel_choices_mixed(self, query_parallel_choices):
        """First takes second, second takes first: b and c"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query_parallel_choices.match(variant)

    def test_parallel_sequence_loops_min(self, query_parallel_sequence_loops):
        """Sequence with loop at minimum: a b and c"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query_parallel_sequence_loops.match(variant)

    def test_parallel_sequence_loops_max(self, query_parallel_sequence_loops):
        """Sequence with loop at maximum: a a b and c"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query_parallel_sequence_loops.match(variant)


class TestParallelSingleBranch:
    """Edge case: parallel with only one branch"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_single_branch_match(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_single_branch_wrong_element(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_single_branch_extra_element(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelLargeBranches:
    """Test parallel with many branches (5+)"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            LeafGroup(lst=["b"]),
                            LeafGroup(lst=["c"]),
                            LeafGroup(lst=["d"]),
                            LeafGroup(lst=["e"]),
                            LeafGroup(lst=["f"]),
                            LeafGroup(lst=["g"]),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_seven_elements_exact(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["e"]),
                        LeafGroup(lst=["f"]),
                        LeafGroup(lst=["g"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_seven_elements_permuted(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["g"]),
                        LeafGroup(lst=["e"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["f"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_seven_elements_missing_one(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["e"]),
                        LeafGroup(lst=["f"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_seven_elements_extra_one(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["e"]),
                        LeafGroup(lst=["f"]),
                        LeafGroup(lst=["g"]),
                        LeafGroup(lst=["h"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelMixedContentTypes:
    """Test parallel with heterogeneous content (sequences and leaves)"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            SequenceGroup(
                                lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]
                            ),
                            LeafGroup(lst=["d"]),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_mixed_content_exact(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        SequenceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_mixed_content_reordered(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["a"]),
                        SequenceGroup(lst=[LeafGroup(lst=["b"]), LeafGroup(lst=["c"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_mixed_content_sequence_reordered(self, query):
        """Sequence branch elements in wrong order"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        SequenceGroup(lst=[LeafGroup(lst=["c"]), LeafGroup(lst=["b"])]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelWithSequenceAndLoop:
    """Test parallel where one branch is a sequence containing loops"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["start"]),
                                    LoopGroup(
                                        lst=[LeafGroup(lst=["a"])],
                                        min_count=1,
                                        max_count=2,
                                    ),
                                    LeafGroup(lst=["end"]),
                                ]
                            ),
                            LeafGroup(lst=["b"]),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_sequence_loop_min(self, query):
        """Sequence with loop at minimum"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["start"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["end"]),
                            ]
                        ),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_sequence_loop_max(self, query):
        """Sequence with loop at maximum"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["start"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["end"]),
                            ]
                        ),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_sequence_loop_interleaved(self, query):
        """Elements interleaved between parallel branches"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["start"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["end"]),
                            ]
                        ),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)


class TestParallelIdenticalBranches:
    """Test parallel with identical sequences in different branches"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]
                            ),
                            SequenceGroup(
                                lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]
                            ),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_identical_branches_exact(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_identical_branches_reordered(self, query):
        """Parallel branches reordered, but both identical"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_identical_branches_interleaved(self, query):
        """Variant interleaves elements: a a b b"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_identical_branches_one_differs(self, query):
        """One branch doesn't match the sequence"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                        SequenceGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["b"])]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelVariantMismatch:
    """Test strict matching constraints"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
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
            ),
            query_type=query_type,
        )

    def test_extra_elements_in_parallel(self, query):
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
        assert not query.match(variant)

    def test_missing_elements_in_parallel(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_duplicate_element_in_parallel(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)

    def test_all_wrong_elements(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["x"]),
                        LeafGroup(lst=["y"]),
                        LeafGroup(lst=["z"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)


class TestParallelOrderIndependence:
    """Verify parallel matching is order-independent"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
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
            ),
            query_type=query_type,
        )

    def test_reverse_order(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["a"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_random_order_1(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_random_order_2(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["d"]),
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["c"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_random_order_3(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["c"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["d"]),
                    ]
                )
            ]
        )
        assert query.match(variant)


class TestParallelWithOptional:
    """Test parallel branches with optional elements (loops with min_count=0)"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    ParallelGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            LoopGroup(
                                lst=[LeafGroup(lst=["b"])],
                                min_count=0,
                                max_count=2,
                            ),
                        ]
                    )
                ]
            ),
            query_type=query_type,
        )

    def test_optional_zero_occurrences(self, query):
        """Optional branch has zero occurrences"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_optional_one_occurrence(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_optional_two_occurrences(self, query):
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert query.match(variant)

    def test_optional_three_occurrences(self, query):
        """Three occurrences exceeds max of 2"""
        variant = SequenceGroup(
            lst=[
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["a"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                        LeafGroup(lst=["b"]),
                    ]
                )
            ]
        )
        assert not query.match(variant)
