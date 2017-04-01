import unittest

from helpers.normalize import normalize_tags, normalize_number


class TestCase(unittest.TestCase):

    def test_normalize_tags(self):
        sample = 'grammar, word meaning'
        assert normalize_tags(sample) == ['grammar', 'word meaning']

        sample = 'grammar'
        assert normalize_tags(sample) == ['grammar']

        sample = 'grammar,word meaning'
        assert normalize_tags(sample) == ['grammar', 'word meaning']

        sample = '   grammar,    word meaning'
        assert normalize_tags(sample) == ['grammar', 'word meaning']

    def test_normalize_number(self):
        sample = 7
        assert normalize_number(sample) == '7'

        sample = 65
        assert normalize_number(sample) == '65'

        sample = 757
        assert normalize_number(sample) == '757'

        sample = 1742
        assert normalize_number(sample) == '1.7k'

        sample = 2000
        assert normalize_number(sample) == '2.0k'

        sample = 89526
        assert normalize_number(sample) == '89.5k'

        sample = 6482359
        assert normalize_number(sample) == '6.4m'

        sample = 895452952
        assert normalize_number(sample) == '895.4m'

        sample = 1000000000
        assert normalize_number(sample) == 'Unlimited!'

if __name__ == '__main__':
    unittest.main()