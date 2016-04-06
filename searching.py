#!/usr/bin/env python
# coding: utf-8

import fileinput

from Engine.Searcher import Searcher
from utils.utils import load_obj, print_error

def main():
    r_index = load_obj("optimized_index")
    searcher = Searcher(r_index)
    docs = load_obj("documents")
    #print_error("readed")

    for line in fileinput.input():
        # TODO всю строку сразу в uft-8 и lower
        line = line.replace("\n", "")
        if '&' in line:
            request = line.split(' & ')
            print_error(request[0])
            print_error(request[1])
            doc_result = searcher.and_words(unicode(request[0], 'utf-8').lower(), unicode(request[1], 'utf-8').lower())
        else:
            doc_result = searcher.find_word(unicode(line, 'utf-8').lower())

        print line
        print len(doc_result)
        for doc_id in doc_result:
            print docs[doc_id]

def test_main(line):
    r_index = load_obj("optimized_index")
    searcher = Searcher(r_index)
    docs = load_obj("documents")
    print("readed")

    if '&' in line:
        request = line.split(' & ')
        print(request[0])
        print(request[1])
        doc_result = searcher.and_words(unicode(request[0], 'utf-8').lower(), unicode(request[1], 'utf-8').lower())
    else:
        print line
        doc_result = searcher.find_word(unicode(line, 'utf-8').lower())

    print len(doc_result)
    for doc_id in doc_result:
        print docs[doc_id]

if __name__ == "__main__":
    main()
    #test_main("Шенгенское & соглашение")