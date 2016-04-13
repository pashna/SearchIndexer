# coding: utf-8

import re
import mmh3
import traceback

class Indexer():

    def __init__(self, count_of_files, encoding):
        self.full_index = {}
        self.documents = []
        self._regex = re.compile(r'\w+', re.U)
        self._encoding = encoding
        self.count_of_files = count_of_files

        for i in range(count_of_files):
            self.full_index[i] = {}

    def _split_text(self, text):
        """
        Function split text to words
        :param text:
        :return:
        """
        text = text.lower()
        words = re.findall(self._regex, text)
        return list(set(words))

    def add_document_indexes(self, text, url, is_print=False):
        # TODO: Maybe, it is good idea to change key from string to hash
        self.documents.append(url)
        doc_id = len(self.documents)-1
        word_list = self._split_text(text.lower())

        for word in word_list:
            #"""
            try:
                word = word.encode('utf-8')

                w_hash = mmh3.hash(word) % self.count_of_files
                if is_print:
                    print word, w_hash
                r_index = self.full_index[w_hash]

                if r_index.has_key(word):
                    r_index[word]["docs"].append(doc_id)
                else:
                    r_index[word] = {}
                    r_index[word]["docs"] = [doc_id]

                if not r_index.has_key('encoding'):
                    r_index['encoding'] = self._encoding

            except Exception as e:
                print "EXCEPRION", word
                traceback.print_exc()