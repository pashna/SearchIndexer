# coding: utf-8
import unittest
import collections

from Engine.VarByteEncoder import VarByteEncoder as vb

class EncodingTest(unittest.TestCase):

    def test_encoding(self):
        a = [1,2,3,4,5,6,7]
        a_encoded = vb.encode(a)
        a_decoded = vb.decode(a_encoded)

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

        self.assertTrue(compare(a_decoded, a))