from .recovery import shouldWait
from assertpy import assert_that

def test_shouldWait_outside_range():
    # given
    ai_pos = (-80, 95)
    edge_pos = (-70, 0)

    # when
    recoverNow = shouldWait(ai_pos, edge_pos[0])

    # then
    assert_that(recoverNow).is_equal_to(True)

def test_shouldWait_inside_range():
    # given
    ai_pos = (-80, 75)
    edge_pos = (-70, 0)

    # when
    recoverNow = shouldWait(ai_pos, edge_pos[0])

    # then
    assert_that(recoverNow).is_equal_to(False)
