import unittest

class ListSearchTests(unittest.TestCase):

    def test_search(self):
        l = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        a = next((l.index(n) for n in l if n > 99), len(l))
        self.assertTrue(a == 9)
