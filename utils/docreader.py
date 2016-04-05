#!/usr/bin/env python

import gzip
import struct
import sys

import document_pb2


class DocumentStreamReader:
    def __init__(self, path):
        if path.endswith('.gz'):
            self.stream = gzip.open(path, 'rb')
        else:
            self.stream = open(path, 'rb')

    def __iter__(self):
        while True:
            sb = self.stream.read(4)
            if sb == '':
                return

            size = struct.unpack('i', sb)[0]
            msg = self.stream.read(size)
            doc = document_pb2.document()
            doc.ParseFromString(msg)
            yield doc


def main():
    arg = sys.argv[1:]
    reader = DocumentStreamReader(sys.argv[1:][0])
    for doc in reader:
        print "%s\tbody: %d, text: %d" % (
            doc.url,
            len(doc.body) if doc.HasField('body') else 0,
            len(doc.text) if doc.HasField('text') else 0
        )


if __name__ == '__main__':
    main()
