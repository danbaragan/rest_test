from mastermind import gameengine

import pytest


@pytest.mark.parametrize("expect_input, expect_output", [
    (([0,1,2,3], [4,4,5,5]), (0,0)), # no match
    (([0,1,2,3], [5,5,1,5]), (0,1)), # 1 color
    (([0,1,2,3], [5,2,5,0]), (0,2)), # 2 color
    (([0,1,2,3], [5,1,5,5]), (1,0)), # 1 full
    (([0,1,2,3], [5,1,5,3]), (2,0)), # 2 full
    (([0,1,2,3], [5,0,2,5]), (1,1)), # 1 full, 1 color
    (([0,1,2,3], [0,3,2,1]), (2,2)), # 2 full, 2 color
    (([0,0,2,3], [5,5,0,0]), (0,2)), # 2x color
    (([0,0,2,3], [3,5,0,0]), (0,3)), # 2x + 1 color
    (([0,1,2,3], [3,2,1,0]), (0,4)), # 4 color
    (([0,0,2,3], [5,0,0,0]), (1,1)), # 1 full, 1 color, 1 color no match
    (([1,0,1,1], [1,1,0,0]), (1,2)), # 1 full, 2 color
    (([0,0,1,1], [0,0,0,1]), (3,0)), # 3 full, 0 color
    (([0,1,2,3], [0,1,2,3]), (4,0)), # 4 full, 0 color
    (([5,4,2,3], [5,4,2,3]), (4,0)), # 4 full, 0 color
    (([5,5,5,5], [5,4,5,5]), (3,0)), # 3 full, 0 color
    (([5,5,5,5], [5,5,5,5]), (4,0)), # 4 full, 0 color
])
def test_compute_answer(expect_input, expect_output):
    game, hand = expect_input
    result = gameengine.compute_answer(game, hand)
    assert expect_output == result
