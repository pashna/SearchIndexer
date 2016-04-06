#!/usr/bin/env python
# coding: utf-8

from Engine.Indexer import Indexer
from utils.docreader import DocumentStreamReader
from utils.utils import save_obj
import sys

def get_reader():
    reader = DocumentStreamReader(sys.stdin)
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
    save_obj(indexer.r_index, "indexer")
    save_obj(indexer.documents, "documents")