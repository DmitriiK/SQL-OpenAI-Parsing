import unittest


from modules.pipeline import analyze_views


class TestParsing(unittest.TestCase):
    def test_view_parsing(self):
        analyze_views()


if __name__ == '__main__':
    print('main')
    unittest.main()
