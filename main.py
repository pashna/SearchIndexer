# coding: utf-8

import sys
from utils.docreader import DocumentStreamReader
from VarByteEncoder import VarByteEncoder as vb
from Indexer import Indexer
from sys import getsizeof


def get_reader():
    reader = DocumentStreamReader("/home/popka/Sphere-Mail/2_term/Searching/3/HW/ts-idx-2016/dump_part001.gz")
    return reader

def create_indexes():

    reader = get_reader()
    indexer = Indexer()

    for doc in reader:
        doc_url = doc.url
        doc_text = doc.text if doc.HasField('text') else 0

        if doc_text != 0:
            indexer.add_document_indexes(text=doc_text, url=doc_url)

    return indexer



if __name__ == "__main__":
    indexer = create_indexes()
    indexer.encode_it()

    """
    fsf = vb.encode_number(532)
    c = fsf+vb.encode_number(1244)
    #.append(vb.encode_number(4214))
    print vb.decode(c)
    """