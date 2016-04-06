# coding: utf-8

import re

class Indexer():

    def __init__(self):
        self.r_index = {}
        self.documents = []
        self._regex = re.compile(r'\w+', re.U)


    def _split_text(self, text):
        """
        Function split text to words
        :param text:
        :return:
        """
        text = text.lower()
        words = re.findall(self._regex, text)
        return list(set(words))

    def add_document_indexes(self, text, url):
        # TODO: Maybe, it is good idea to change key from string to hash
        self.documents.append(url)
        doc_id = len(self.documents)-1

        word_list = self._split_text(text.lower())
        for word in word_list:

            if self.r_index.has_key(word):
                self.r_index[word]["docs"].append(doc_id)
            else:
                self.r_index[word] = {}
                self.r_index[word]["docs"] = [doc_id]
