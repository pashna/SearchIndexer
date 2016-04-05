# coding: utf-8
import collections
import unittest

from Engine.Optimizer import Optimizer


class OptimizerTest(unittest.TestCase):

    def test_diff(self):

        optimizer = Optimizer()
        r_index = \
            {
                "a": {
                    "docs": [1, 5, 7, 9],
                }
                ,
                "b": {
                    "docs": [10, 52, 356],
                }
            }
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

        r_index = optimizer.create_jump_table(r_index, jump_step=1)
        self.assertTrue(compare(r_index["a"]["docs"], [1, 4, 2, 2]))
        self.assertTrue(compare(r_index["b"]["docs"], [10, 42, 304]))


    def test_jump_table(self):

        optimizer = Optimizer()
        r_index = \
            {
                "a": {
                    "docs": [0, 1, 2, 3, 4, 5, 6, 7],
                }
            }

        r_index = optimizer.create_jump_table(r_index, jump_step=2)
        self.assertTrue(cmp(r_index["a"]["jump_table"], {"jump_step": 2, 2:2, 4:4, 6:6}) == 0)



