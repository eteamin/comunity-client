import unittest

from helpers.normalize import normalize_tag


class TestCase(unittest.TestCase):

    def test_normalize_tags(self):
        sample1 = 'grammar, word meaning'
        assert normalize_tag(sample1) == ['grammar', 'word meaning']

        sample2 = 'grammar'
        assert normalize_tag(sample2) == ['grammar']

        sample3 = 'grammar,word meaning'
        assert normalize_tag(sample3) == ['grammar', 'word meaning']

        sample4 = '   grammar,    word meaning'
        assert normalize_tag(sample4) == ['grammar', 'word meaning']
