# coding: utf-8

import unittest
from Engine.Optimizer import Optimizer
from Engine.Searcher import Searcher

class SearcherTests(unittest.TestCase):

    def search_test(self):

        optimizer = Optimizer()
        r_index = \
            {
                "a": {
                    "docs": [0, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 36],
                }
                ,
                "b": {
                    "docs": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                }
            }

        r_index = optimizer.create_jump_table(r_index, jump_step=3)
        optimizer.encode_it(r_index)
        searcher = Searcher(r_index)
        docs = searcher.and_words("a", "b")
        123-12