#!/usr/bin/env python
# coding: utf-8

from Engine.VarByteEncoder import VarByteEncoder
from Engine.Simple9 import Simple9
import fileinput
from Engine.QueryParser import QueryExecutor

from Engine.Searcher import Searcher
from utils.utils import load_obj, print_error

def main():
    r_index = load_obj("optimized_index")
    searcher = Searcher(r_index, Simple9())
    docs = load_obj("documents")
    #print_error("readed")

    for line in fileinput.input():
        # TODO всю строку сразу в uft-8 и lower
        line = line.replace("\n", "")
        if '&' in line:
            request = line.split(' & ')
            for i in range(len(request)):
                request[i] = unicode(request[i], 'utf-8').lower()

            doc_result = searcher.and_word_list(request)
        else:
            doc_result = searcher.find_word(unicode(line, 'utf-8').lower())


        print line
        print len(doc_result)
        for doc_id in doc_result:
            print docs[doc_id]


def test_main(line):
    r_index = load_obj("optimized_index")
    searcher = Searcher(r_index, Simple9())
    docs = load_obj("documents")

    print("readed")
    qe = QueryExecutor(searcher)
    start_time = time.time()
    doc_result = qe.query(line)
    """
    if '&' in line:

        request = line.split(' & ')
        for i in range(len(request)):
            request[i] = unicode(request[i], 'utf-8').lower()

        doc_result = searcher.and_word_list(request)


    else:
        doc_result = searcher.find_word(unicode(line, 'utf-8').lower())
    """
    print line
    print len(doc_result)
    for doc_id in doc_result:
        print docs[doc_id]

    print("--- %s seconds ---" % (time.time() - start_time))


import time

if __name__ == "__main__":
    #main()
    
    print test_main(u"путин & !россия & !крым")