from .recovery import edgeAngleCalc
from assertpy import assert_that

def test_edgeAngleCalc_left_of_stage():
    # given
    ai_pos = (-80, 0)
    edge_pos = (-70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(1, 0.001)
    assert_that(y_dir).is_close_to(0, 0.001)

def test_edgeAngleCalc_right_of_stage():
    # given
    ai_pos = (80, 0)
    edge_pos = (70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(-1, 0.001)
    assert_that(y_dir).is_close_to(0, 0.001)


def test_edgeAngleCalc_straight_up_left_of_stage():
    # given
    ai_pos = (-70, -30)
    edge_pos = (-70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(0, 0.001)
    assert_that(y_dir).is_close_to(1, 0.001)


def test_edgeAngleCalc_straight_up_right_of_stage():
    # given
    ai_pos = (70, -30)
    edge_pos = (70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(0, 0.001)
    assert_that(y_dir).is_close_to(1, 0.001)


def test_edgeAngleCalc_45_deg_up_left_of_stage():
    # given
    ai_pos = (-80, 10)
    edge_pos = (-70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(0.70710678, 0.001)
    assert_that(y_dir).is_close_to(-0.70710678, 0.001)


def test_edgeAngleCalc_45_deg_down_left_of_stage():
    # given
    ai_pos = (-80, -10)
    edge_pos = (-70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(0.70710678, 0.001)
    assert_that(y_dir).is_close_to(0.70710678, 0.001)


def test_edgeAngleCalc_45_deg_up_right_of_stage():
    # given
    ai_pos = (80, 10)
    edge_pos = (70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(-0.70710678, 0.001)
    assert_that(y_dir).is_close_to(-0.70710678, 0.001)


def test_edgeAngleCalc_45_deg_down_right_of_stage():
    # given
    ai_pos = (80, -10)
    edge_pos = (70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(-0.70710678, 0.001)
    assert_that(y_dir).is_close_to(0.70710678, 0.001)

def test_edgeAngleCalc_under_right_of_stage():
    # given
    ai_pos = (60, -10)
    edge_pos = (70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(-0.70710678, 0.001)
    assert_that(y_dir).is_close_to(0.70710678, 0.001)
def test_edgeAngleCalc_under_left_of_stage():
    # given
    ai_pos = (-60, -10)
    edge_pos = (-70, 0)

    # when
    x_dir,y_dir = edgeAngleCalc(ai_pos, edge_pos[0])

    # then
    assert_that(x_dir).is_close_to(0.70710678, 0.001)
    assert_that(y_dir).is_close_to(0.70710678, 0.001)