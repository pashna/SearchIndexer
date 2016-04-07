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
