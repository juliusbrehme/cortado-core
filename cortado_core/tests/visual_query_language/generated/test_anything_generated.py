"""
AI generated tests for AnythingGroup operator include:
- TestSingleAnythingBasic: Basic single AnythingGroup between two elements. Tests minimal and extended content matching
- TestMultipleAnythingSequential: Multiple consecutive AnythingGroup operators. Each must match at least one element
- TestAnythingInNestedSequence: AnythingGroup inside nested sequences. Tests proper scope isolation
- TestAnythingWithParallel: AnythingGroup matching parallel groups and sequential content. Tests complex branching
- TestAnythingWithLoop: AnythingGroup at start/middle/end of looped sequences. Handles repetition contexts
- TestAnythingWithChoice: AnythingGroup combined with choice groups. Tests interaction with alternatives
- TestMultipleAnythingWithElements: Multiple AnythingGroup with anchoring elements between them. Tests backtracking
- TestAnythingInParallel: AnythingGroup inside parallel group branches. Tests concurrent matching
- TestAnythingAtBoundaries: AnythingGroup at start and end of sequences. Tests edge positioning
- TestDeepNesting: AnythingGroup deeply nested in complex structures. Tests recursion handling
- TestAnythingWithMixedOperators: AnythingGroup combined with loops, choices, and parallel groups simultaneously
- TestComplexBacktracking: Intricate backtracking scenarios with multiple AnythingGroup instances. Tests greedy vs minimal matching
"""

import pytest
from cortado_core.utils.split_graph import (
    SequenceGroup,
    LeafGroup,
    ParallelGroup,
    AnythingGroup,
    OptionalGroup,
    LoopGroup,
    ChoiceGroup,
)
from cortado_core.visual_query_language.query import create_query_instance
from cortado_core.tests.visual_query_language.query_type_fixture import query_type


class TestSingleAnythingBasic:
    """Test single AnythingGroup in simplest form"""

    @pytest.fixture
    def query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[LeafGroup(lst=["a"]), AnythingGroup(), LeafGroup(lst=["b"])]
            ),
            query_type=query_type,
        )

    def test_single_element_matches(self, query):
        """a x b - single element between"""
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["b"])]
        )
        assert query.match(variant)

    def test_multiple_elements_match(self, query):
        """a x y z b - multiple elements between"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert query.match(variant)

    def test_no_element_fails(self, query):
        """a b - no element between, should fail"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])])
        assert not query.match(variant)

    def test_missing_end_element_fails(self, query):
        """a x - missing b"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"])])
        assert not query.match(variant)

    def test_missing_start_element_fails(self, query):
        """x b - missing a"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["b"])])
        assert not query.match(variant)

    def test_with_many_elements_between(self, query):
        """a x y z w v u t b - 7 elements between"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["v"]),
                LeafGroup(lst=["u"]),
                LeafGroup(lst=["t"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert query.match(variant)


class TestMultipleAnythingSequential:
    """Test multiple consecutive AnythingGroup operators"""

    @pytest.fixture
    def double_anything_query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def triple_anything_query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    AnythingGroup(),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                ]
            ),
            query_type=query_type,
        )

    def test_double_anything_two_elements(self, double_anything_query):
        """a x y b - two elements for two AnythingGroups"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert double_anything_query.match(variant)

    def test_double_anything_one_element_fails(self, double_anything_query):
        """a x b - only one element for two AnythingGroups, should fail"""
        variant = SequenceGroup(
            lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"]), LeafGroup(lst=["b"])]
        )
        assert not double_anything_query.match(variant)

    def test_double_anything_many_elements(self, double_anything_query):
        """a x y z w b - many elements for two AnythingGroups"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert double_anything_query.match(variant)

    def test_triple_anything_three_elements(self, triple_anything_query):
        """a x y z b - exactly three elements"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert triple_anything_query.match(variant)

    def test_triple_anything_many_elements(self, triple_anything_query):
        """a x y z w v u b - more than three elements"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["v"]),
                LeafGroup(lst=["u"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert triple_anything_query.match(variant)


class TestAnythingInNestedSequence:
    """Test AnythingGroup inside nested sequences"""

    @pytest.fixture
    def nested_query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    SequenceGroup(
                        lst=[
                            LeafGroup(lst=["x"]),
                            AnythingGroup(),
                            LeafGroup(lst=["y"]),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_nested_anything_simple(self, nested_query):
        """start x a y end - simple nested"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert nested_query.match(variant)

    def test_nested_anything_multiple_elements(self, nested_query):
        """start x a b c d y end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert nested_query.match(variant)

    def test_nested_anything_no_element_fails(self, nested_query):
        """start x y end - no element between x and y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert not nested_query.match(variant)


class TestAnythingWithParallel:
    """Test AnythingGroup matching parallel groups and complex content"""

    @pytest.fixture
    def anything_parallel_query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                ]
            ),
            query_type=query_type,
        )

    def test_anything_matches_parallel(self, anything_parallel_query):
        """a (x || y) b - parallel group matches as single element"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert anything_parallel_query.match(variant)

    def test_anything_matches_parallel_and_leaves(self, anything_parallel_query):
        """a x (y || z) w b - parallel with other elements"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                ParallelGroup(lst=[LeafGroup(lst=["y"]), LeafGroup(lst=["z"])]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert anything_parallel_query.match(variant)

    def test_anything_matches_nested_parallel(self, anything_parallel_query):
        """a (x || (y z)) b"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        LeafGroup(lst=["x"]),
                        SequenceGroup(lst=[LeafGroup(lst=["y"]), LeafGroup(lst=["z"])]),
                    ]
                ),
                LeafGroup(lst=["b"]),
            ]
        )
        assert anything_parallel_query.match(variant)


class TestAnythingWithLoop:
    """Test AnythingGroup in contexts with loops"""

    @pytest.fixture
    def anything_before_loop(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    AnythingGroup(),
                    LoopGroup(
                        lst=[LeafGroup(lst=["x"])],
                        min_count=2,
                        max_count=3,
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def anything_in_loop_sequence(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["b"]),
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

    def test_anything_before_loop_min(self, anything_before_loop):
        """start a x x end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_before_loop.match(variant)

    def test_anything_before_loop_max(self, anything_before_loop):
        """start a b c x x x end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_before_loop.match(variant)

    def test_anything_in_loop_min(self, anything_in_loop_sequence):
        """start a x b end - loop executes once"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_in_loop_sequence.match(variant)

    def test_anything_in_loop_max(self, anything_in_loop_sequence):
        """start a x b a y z b end - loop executes twice with different content"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_in_loop_sequence.match(variant)


class TestAnythingWithChoice:
    """Test AnythingGroup combined with choice groups"""

    @pytest.fixture
    def anything_with_choice(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    ChoiceGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["y"])]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def anything_inside_choice_sequence(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    ChoiceGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["x"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["y"]),
                                ]
                            ),
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["p"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["q"]),
                                ]
                            ),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_anything_before_choice_x(self, anything_with_choice):
        """a content x - choice picks x"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["m"]),
                LeafGroup(lst=["x"]),
            ]
        )
        assert anything_with_choice.match(variant)

    def test_anything_before_choice_y(self, anything_with_choice):
        """a content y - choice picks y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["m"]),
                LeafGroup(lst=["y"]),
            ]
        )
        assert anything_with_choice.match(variant)

    def test_anything_before_choice_multi(self, anything_with_choice):
        """a x y m z x - anything matches multiple elements before choice"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["m"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["x"]),
            ]
        )
        assert anything_with_choice.match(variant)

    def test_anything_inside_choice_first_branch(self, anything_inside_choice_sequence):
        """start x a y end - first choice branch"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_inside_choice_sequence.match(variant)

    def test_anything_inside_choice_second_branch(
        self, anything_inside_choice_sequence
    ):
        """start p m n q end - second choice branch"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["p"]),
                LeafGroup(lst=["m"]),
                LeafGroup(lst=["n"]),
                LeafGroup(lst=["q"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_inside_choice_sequence.match(variant)


class TestMultipleAnythingWithElements:
    """Test multiple AnythingGroup instances with anchoring elements between"""

    @pytest.fixture
    def multiple_anything_anchored(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                    AnythingGroup(),
                    LeafGroup(lst=["c"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def three_anything_anchored(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                    AnythingGroup(),
                    LeafGroup(lst=["c"]),
                    AnythingGroup(),
                    LeafGroup(lst=["d"]),
                ]
            ),
            query_type=query_type,
        )

    def test_two_anything_minimal(self, multiple_anything_anchored):
        """a x b y c - minimal content for each anything"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert multiple_anything_anchored.match(variant)

    def test_two_anything_first_extended(self, multiple_anything_anchored):
        """a x y z b w c"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert multiple_anything_anchored.match(variant)

    def test_two_anything_both_extended(self, multiple_anything_anchored):
        """a x y b z w c"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert multiple_anything_anchored.match(variant)

    def test_two_anything_backtrack_scenario(self, multiple_anything_anchored):
        """a b b y c - first anything could greedily consume second b,
        but backtracking ensures match"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["c"]),
            ]
        )
        assert multiple_anything_anchored.match(variant)

    def test_three_anything_minimal(self, three_anything_anchored):
        """a x b y c z d"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["d"]),
            ]
        )
        assert three_anything_anchored.match(variant)

    def test_three_anything_mixed(self, three_anything_anchored):
        """a x y b z c w v u d"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["v"]),
                LeafGroup(lst=["u"]),
                LeafGroup(lst=["d"]),
            ]
        )
        assert three_anything_anchored.match(variant)


class TestAnythingInParallel:
    """Test AnythingGroup inside parallel group branches"""

    @pytest.fixture
    def anything_in_parallel_branch(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["a"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["b"]),
                                ]
                            ),
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["x"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["y"]),
                                ]
                            ),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    def test_anything_in_parallel_both_minimal(self, anything_in_parallel_branch):
        """start (a c b || x z y) end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["c"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["x"]),
                                LeafGroup(lst=["z"]),
                                LeafGroup(lst=["y"]),
                            ]
                        ),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_in_parallel_branch.match(variant)

    def test_anything_in_parallel_different_lengths(self, anything_in_parallel_branch):
        """start (a c d b || x z w y) end - different content lengths"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["c"]),
                                LeafGroup(lst=["d"]),
                                LeafGroup(lst=["b"]),
                            ]
                        ),
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["x"]),
                                LeafGroup(lst=["z"]),
                                LeafGroup(lst=["w"]),
                                LeafGroup(lst=["y"]),
                            ]
                        ),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert anything_in_parallel_branch.match(variant)


class TestAnythingAtBoundaries:
    """Test AnythingGroup at start and end of sequences"""

    @pytest.fixture
    def anything_at_start(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    AnythingGroup(),
                    LeafGroup(lst=["a"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def anything_at_end(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def anything_at_both_boundaries(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    AnythingGroup(),
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                ]
            ),
            query_type=query_type,
        )

    def test_anything_at_start_single(self, anything_at_start):
        """x a"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["x"]), LeafGroup(lst=["a"])])
        assert anything_at_start.match(variant)

    def test_anything_at_start_multiple(self, anything_at_start):
        """x y z a"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["a"]),
            ]
        )
        assert anything_at_start.match(variant)

    def test_anything_at_end_single(self, anything_at_end):
        """a x"""
        variant = SequenceGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["x"])])
        assert anything_at_end.match(variant)

    def test_anything_at_end_multiple(self, anything_at_end):
        """a x y z"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
            ]
        )
        assert anything_at_end.match(variant)

    def test_anything_at_both_boundaries_minimal(self, anything_at_both_boundaries):
        """x a y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["y"]),
            ]
        )
        assert anything_at_both_boundaries.match(variant)

    def test_anything_at_both_boundaries_extended(self, anything_at_both_boundaries):
        """x y a z w"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["w"]),
            ]
        )
        assert anything_at_both_boundaries.match(variant)


class TestDeepNesting:
    """Test AnythingGroup deeply nested in complex structures"""

    @pytest.fixture
    def deeply_nested_query(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    SequenceGroup(
                        lst=[
                            LeafGroup(lst=["a"]),
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["b"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["c"]),
                                ]
                            ),
                            LeafGroup(lst=["d"]),
                        ]
                    ),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def complex_nested_with_loop_parallel(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    ParallelGroup(
                                        lst=[
                                            SequenceGroup(
                                                lst=[
                                                    LeafGroup(lst=["x"]),
                                                    AnythingGroup(),
                                                    LeafGroup(lst=["y"]),
                                                ]
                                            ),
                                            LeafGroup(lst=["z"]),
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

    def test_double_nested_sequence(self, deeply_nested_query):
        """start a b x c d end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert deeply_nested_query.match(variant)

    def test_double_nested_sequence_extended(self, deeply_nested_query):
        """start a b x y z c d end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["d"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert deeply_nested_query.match(variant)

    def test_complex_nested_loop_parallel_min(self, complex_nested_with_loop_parallel):
        """start (x a y || z) end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["x"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["y"]),
                            ]
                        ),
                        LeafGroup(lst=["z"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert complex_nested_with_loop_parallel.match(variant)

    def test_complex_nested_loop_parallel_max(self, complex_nested_with_loop_parallel):
        """start (x a b y || z) (x c d e y || z) end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["x"]),
                                LeafGroup(lst=["a"]),
                                LeafGroup(lst=["b"]),
                                LeafGroup(lst=["y"]),
                            ]
                        ),
                        LeafGroup(lst=["z"]),
                    ]
                ),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["x"]),
                                LeafGroup(lst=["c"]),
                                LeafGroup(lst=["d"]),
                                LeafGroup(lst=["e"]),
                                LeafGroup(lst=["y"]),
                            ]
                        ),
                        LeafGroup(lst=["z"]),
                    ]
                ),
                LeafGroup(lst=["end"]),
            ]
        )
        assert complex_nested_with_loop_parallel.match(variant)


class TestAnythingWithMixedOperators:
    """Test AnythingGroup with loops, choices, and parallel groups simultaneously"""

    @pytest.fixture
    def mixed_all_operators(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    AnythingGroup(),
                    LoopGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    ChoiceGroup(
                                        lst=[
                                            ParallelGroup(
                                                lst=[
                                                    LeafGroup(lst=["a"]),
                                                    LeafGroup(lst=["b"]),
                                                ]
                                            ),
                                            LeafGroup(lst=["c"]),
                                        ]
                                    ),
                                    AnythingGroup(),
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

    def test_mixed_operators_first_branch_min(self, mixed_all_operators):
        """start pre (a || b) post end - choice picks parallel"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["pre"]),
                ParallelGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                LeafGroup(lst=["post"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert mixed_all_operators.match(variant)

    def test_mixed_operators_second_branch_min(self, mixed_all_operators):
        """start pre c post end - choice picks leaf"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["pre"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["post"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert mixed_all_operators.match(variant)

    def test_mixed_operators_loop_max_parallel(self, mixed_all_operators):
        """start x (a || b) y (a || b) z end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                ParallelGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                LeafGroup(lst=["y"]),
                ParallelGroup(lst=[LeafGroup(lst=["a"]), LeafGroup(lst=["b"])]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert mixed_all_operators.match(variant)

    def test_mixed_operators_loop_max_choice(self, mixed_all_operators):
        """start x c y1 y2 c z end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["y1"]),
                LeafGroup(lst=["y2"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert mixed_all_operators.match(variant)


class TestComplexBacktracking:
    """Test intricate backtracking scenarios with multiple AnythingGroup instances"""

    @pytest.fixture
    def complex_backtrack_scenario_1(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                    AnythingGroup(),
                    LeafGroup(lst=["b"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def complex_backtrack_scenario_2(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["start"]),
                    AnythingGroup(),
                    LeafGroup(lst=["x"]),
                    AnythingGroup(),
                    LeafGroup(lst=["x"]),
                    AnythingGroup(),
                    LeafGroup(lst=["end"]),
                ]
            ),
            query_type=query_type,
        )

    @pytest.fixture
    def complex_backtrack_with_parallel(self, query_type):
        return create_query_instance(
            SequenceGroup(
                lst=[
                    LeafGroup(lst=["a"]),
                    AnythingGroup(),
                    ParallelGroup(
                        lst=[
                            SequenceGroup(
                                lst=[
                                    LeafGroup(lst=["b"]),
                                    AnythingGroup(),
                                    LeafGroup(lst=["c"]),
                                ]
                            ),
                            LeafGroup(lst=["d"]),
                        ]
                    ),
                    AnythingGroup(),
                    LeafGroup(lst=["e"]),
                ]
            ),
            query_type=query_type,
        )

    def test_ambiguous_element_at_anchor(self, complex_backtrack_scenario_1):
        """a x b y b - first anything matches x, second matches y"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert complex_backtrack_scenario_1.match(variant)

    def test_complex_multiway_backtrack(self, complex_backtrack_scenario_1):
        """a x y b z w b"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["b"]),
            ]
        )
        assert complex_backtrack_scenario_1.match(variant)

    def test_three_anything_with_repeated_anchor(self, complex_backtrack_scenario_2):
        """start a x b x c x end"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["b"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["c"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert complex_backtrack_scenario_2.match(variant)

    def test_three_anything_ambiguous_distribution(self, complex_backtrack_scenario_2):
        """start x x x x x x end - 6 x's, but only 3 anchors and 3 anything's"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["start"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["end"]),
            ]
        )
        assert complex_backtrack_scenario_2.match(variant)

    def test_backtrack_with_parallel_in_middle(self, complex_backtrack_with_parallel):
        """a x (b y c || d) z e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["b"]),
                                LeafGroup(lst=["y"]),
                                LeafGroup(lst=["c"]),
                            ]
                        ),
                        LeafGroup(lst=["d"]),
                    ]
                ),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert complex_backtrack_with_parallel.match(variant)

    def test_backtrack_with_complex_parallel(self, complex_backtrack_with_parallel):
        """a x y (b m n c || d) w v e"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                LeafGroup(lst=["x"]),
                LeafGroup(lst=["y"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["b"]),
                                LeafGroup(lst=["m"]),
                                LeafGroup(lst=["n"]),
                                LeafGroup(lst=["c"]),
                            ]
                        ),
                        LeafGroup(lst=["d"]),
                    ]
                ),
                LeafGroup(lst=["w"]),
                LeafGroup(lst=["v"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert complex_backtrack_with_parallel.match(variant)

    def test_backtrack_without_middle_element(self, complex_backtrack_with_parallel):
        """a x (b c || d) z e - nothing between anything and parallel"""
        variant = SequenceGroup(
            lst=[
                LeafGroup(lst=["a"]),
                ParallelGroup(
                    lst=[
                        SequenceGroup(
                            lst=[
                                LeafGroup(lst=["b"]),
                                LeafGroup(lst=["c"]),
                            ]
                        ),
                        LeafGroup(lst=["d"]),
                    ]
                ),
                LeafGroup(lst=["z"]),
                LeafGroup(lst=["e"]),
            ]
        )
        assert not complex_backtrack_with_parallel.match(variant)
