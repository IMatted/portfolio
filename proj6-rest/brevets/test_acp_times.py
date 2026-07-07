import acp_times
import arrow

START = "2026-05-06T00:00:00+00:00"

def test_start_control():
    """RUSA Rule: 0km control times are fixed"""
    open_t = acp_times.open_time(0, 200, START)
    close_t = acp_times.close_time(0, 200, START)
    assert open_t == START
    assert close_t == arrow.get(START).shift(hours=1).isoformat()

def test_under_60km():
    """RUSA Rule: special closing formula for controls < 60km"""
    close_t = acp_times.close_time(20, 200, START)
    expected = arrow.get(START).shift(hours=2).isoformat()
    assert close_t == expected

def test_math_logic():
    """test the mathematical logic associated with the mid-points"""
    open_t = acp_times.open_time(400, 400, START)
    expected = arrow.get(START).shift(hours=12, minutes=8).isoformat()
    assert open_t == expected

def test_brevet_cap():
    """makes sure that a brevet cannot go past its allocated distance"""
    time_200 = acp_times.open_time(200, 200, START)
    time_210 = acp_times.open_time(210, 200, START)
    assert time_200 == time_210

def test_finish_overrides():
    """RUSA Rule: time to finish 1000km is 75 hours"""
    close_t = acp_times.close_time(1000, 1000, START)
    expected = arrow.get(START).shift(hours=75).isoformat()
    assert close_t == expected