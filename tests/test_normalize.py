import unittest

from helpers.normalize import normalize_tags


class TestCase(unittest.TestCase):

    def test_normalize_tags(self):
        sample1 = 'grammar, word meaning'
        assert normalize_tags(sample1) == ['grammar', 'word meaning']

        sample2 = 'grammar'
        assert normalize_tags(sample2) == ['grammar']

        sample3 = 'grammar,word meaning'
        assert normalize_tags(sample3) == ['grammar', 'word meaning']

        sample4 = '   grammar,    word meaning'
        assert normalize_tags(sample4) == ['grammar', 'word meaning']
