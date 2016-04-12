# coding: utf-8

import unittest
from Engine.Optimizer import Optimizer
from Engine.Searcher import Searcher
import collections
import copy
from Engine.Simple9 import Simple9

class SearcherTests(unittest.TestCase):


    def search_test(self):

        optimizer = Optimizer(Simple9())
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
        searcher = Searcher(r_index, Simple9())
        docs = searcher._and_words("a", "b")
        self.assertTrue(len(docs) == 5)



    def test_find_interval(self):
        jump_values = [6, 13, 25, 80]
        jump_step = 5
        s = Searcher(r_index=None, encoder=Simple9())

        interval = s._find_interval(jump_values, 3, jump_step)
        self.assertTrue(interval[0]==0 and interval[1]==5 and interval[2]==-1)

        interval = s._find_interval(jump_values, 7, jump_step)
        self.assertTrue(interval[0]==5 and interval[1]==10 and interval[2]==6)

        interval = s._find_interval(jump_values, 88, jump_step)
        self.assertTrue(interval[0]==20 and interval[1]==-1 and interval[2]==80)


    def test_empty(self):
        jump_values = []
        jump_step = 5
        s = Searcher(r_index=None, encoder=Simple9())

        interval = s._find_interval(jump_values, 3, jump_step)
        self.assertTrue(interval[0]==0 and interval[1]==5 and interval[2]==-1)


    def test_find_word(self):
        optimizer = Optimizer(Simple9())
        lst = [0, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 36]
        r_index = \
            {
                "a": {
                    "docs": copy.copy(lst),
                }
                ,
                "b": {
                    "docs": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                }
            }

        r_index = optimizer.create_jump_table(r_index, jump_step=3)
        optimizer.encode_it(r_index)
        searcher = Searcher(r_index, Simple9())
        docs = searcher.find_word("a")
        self.assertTrue(len(docs) == len(lst))


    def test_docs_and_word(self):
        optimizer = Optimizer(Simple9())
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
        searcher1 = Searcher(r_index, Simple9())
        docs = searcher1.find_word("a")
        docs_and_docs = searcher1.and_word_and_docs(docs, "b")

        seacher2 = Searcher(r_index, Simple9())
        docs_and_words = seacher2._and_words("a", "b")

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        self.assertTrue(compare(docs_and_docs, docs_and_words))


    def test_or(self):
        optimizer = Optimizer(Simple9())
        r_index = \
            {
                "a": {
                    "docs": [0, 5, 7,],
                }
                ,
                "b": {
                    "docs": [0,3,4,5,],
                }
            }

        r_index = optimizer.create_jump_table(r_index, jump_step=3)
        optimizer.encode_it(r_index)
        searcher = Searcher(r_index, Simple9())

        docs = searcher.or_("a", "b")

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        self.assertTrue(compare(docs, [0,3,4,5,7]))


    def test_and_not(self):
        optimizer = Optimizer(Simple9())
        r_index = \
            {
                "a": {
                    "docs": [0, 5, 7,],
                }
                ,
                "b": {
                    "docs": [0,3,4,5,],
                }
            }

        r_index = optimizer.create_jump_table(r_index, jump_step=3)
        optimizer.encode_it(r_index)
        searcher = Searcher(r_index, Simple9())

        docs = searcher.and_not("a", "b")

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        self.assertTrue(compare(docs, [7]))


    def test_not_and(self):
        optimizer = Optimizer(Simple9())
        r_index = \
            {
                "a": {
                    "docs": [1,2,3,4],
                }
                ,
                "b": {
                    "docs": [0, 2,4,5],
                }
            }

        r_index = optimizer.create_jump_table(r_index, jump_step=3)
        optimizer.encode_it(r_index)
        searcher = Searcher(r_index, Simple9())

        docs = searcher.not_and("a", "b")

        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        self.assertTrue(compare(docs, [0,5]))