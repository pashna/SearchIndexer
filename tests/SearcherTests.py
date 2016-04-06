# coding: utf-8

import unittest
from Engine.Optimizer import Optimizer
from Engine.Searcher import Searcher
import collections

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
        self.assertTrue(len(docs) == 5)



    def test_find_interval(self):
        jump_values = [6, 13, 25, 80]
        jump_step = 5
        s = Searcher(r_index=None)

        interval = s._find_interval(jump_values, 3, jump_step)
        self.assertTrue(interval[0]==0 and interval[1]==5 and interval[2]==-1)

        interval = s._find_interval(jump_values, 7, jump_step)
        self.assertTrue(interval[0]==5 and interval[1]==10 and interval[2]==6)

        interval = s._find_interval(jump_values, 88, jump_step)
        self.assertTrue(interval[0]==20 and interval[1]==-1 and interval[2]==80)


    def test_empty(self):
        jump_values = []
        jump_step = 5
        s = Searcher(r_index=None)

        interval = s._find_interval(jump_values, 3, jump_step)
        self.assertTrue(interval[0]==0 and interval[1]==5 and interval[2]==-1)


    def test_find_word(self):
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
        docs = searcher.find_word("a")
        self.assertTrue(len(r_index["a"]["docs"]) == len(docs))


    def test_docs_and_word(self):
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
        searcher1 = Searcher(r_index)
        docs = searcher1.find_word("a")
        docs_and_docs = searcher1.and_word_and_docs(docs, "b")

        seacher2 = Searcher(r_index)
        docs_and_words = seacher2.and_words("a", "b")

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        self.assertTrue(compare(docs_and_docs, docs_and_words))

