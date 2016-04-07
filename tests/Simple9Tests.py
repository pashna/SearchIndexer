# coding: utf-8

import unittest

import collections
from Engine.Simple9 import Simple9

class Simple9Tests(unittest.TestCase):

    def test_simple9(self):
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

        encoder = Simple9()

        a = [1,2,42,14,51,2351,32523,1242531,132412341,4242]
        encoded = encoder.encode(a)
        b = encoder.decode(encoded)
        self.assertTrue(compare(a, b))


    def test_vlasti(self):
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        docs = [10, 7, 3, 1, 5, 4, 19, 2, 9, 2, 9, 20, 1, 14, 13, 4, 4, 3, 8, 15, 1, 9, 2, 3, 2, 15, 33, 10, 8, 20, 8, 3, 4, 1, 5, 1, 14, 23, 1, 16, 13, 14, 11, 7, 20, 5, 33, 3, 1, 12, 10, 13, 7, 1, 7, 7, 3, 2, 3, 14, 15, 5, 6, 3, 3, 1, 1, 6, 3, 12, 9, 10, 9, 1, 1, 11, 6, 8, 3, 2, 5, 9, 3, 5, 13, 8, 15, 13, 17, 3, 14, 3, 3, 6, 10, 1, 16, 10, 6, 16, 13, 19, 26, 10, 6, 1, 5, 2, 4, 11, 1, 3, 11, 14, 10, 3, 11, 3, 21, 1, 6, 21, 1, 7, 9, 20, 5, 4, 8, 2, 1, 23, 1, 2, 5, 23, 3, 10, 6, 4, 10, 20, 13, 10, 1, 24, 5, 5, 2, 2, 4, 6, 1, 1, 12, 6]

        encoder = Simple9()
        encoded = encoder.encode(docs)
        b = encoder.decode(encoded)
        self.assertTrue(compare(docs, b))