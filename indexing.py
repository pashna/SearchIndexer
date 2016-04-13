#!/usr/bin/env python
# coding: utf-8

from Engine.Indexer import Indexer
from utils.docreader import DocumentStreamReader
from utils.utils import save_obj
import sys
import traceback



COUNT_OF_FILES = 40

def get_reader():
    reader = DocumentStreamReader(sys.stdin)
    return reader

def create_indexes(encoding):

    reader = get_reader()
    indexer = Indexer(COUNT_OF_FILES, encoding)

    for doc in reader:
        doc_url = doc.url
        doc_text = doc.text if doc.HasField('text') else 0

        if doc_text != 0:
            indexer.add_document_indexes(text=doc_text, url=doc_url)

    return indexer


if __name__ == "__main__":
    encoding = sys.argv[1]
    indexer = create_indexes(encoding)
    for key, r_index in indexer.full_index.iteritems():
        if key != "encoding":
            save_obj(r_index, "indexer_"+str(key))

    save_obj(indexer.documents, "documents")