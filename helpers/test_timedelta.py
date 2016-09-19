import unittest
from datetime import datetime

from timedelta import tell_time_ago


class TestCase(unittest.TestCase):
    def test_timedelta(self):
        a_year_ago = datetime(2015, 5, 12, 23, 15, 15, 53000)
        assert tell_time_ago(a_year_ago) == 'A year ago'
