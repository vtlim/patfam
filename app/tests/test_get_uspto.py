"""
test_get_uspto.py
"""
import sys, os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.." ))
from get_uspto import get_uspto_continuity

def test_get_uspto():
    result = get_uspto_continuity("09418640", "application")
    # check that result has the 'child' key
    assert 'child' in result
    assert result['child'][0] == 'PCT/US00/27963'

def test_get_uspto_error():
    result = get_uspto_continuity("000", "publication")
    assert result == "ERROR"
