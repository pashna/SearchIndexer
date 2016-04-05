# coding: utf-8

from VarByteEncoder import VarByteEncoder as vb
import re

class Indexer():

    def __init__(self):
        self.r_index = {}
        self.documents = []
        self._regex = re.compile(r'\w+', re.U)


    def _split_text(self, text):
        """
        Функция разбивает текст на слова
        :param text:
        :return:
        """
        words = re.findall(self._regex, text)
        return map(lambda s: s.lower(), words)


    def add_document_indexes(self, text, url):
        # TODO: Возможно, имеет смысл заменить ключи у word_list со строк на что-нибудь другое
        self.documents.append(url)
        doc_id = len(self.documents)-1

        word_list = self._split_text(text.lower())
        for word in word_list:

            if self.r_index.has_key(word):
                last_doc = self.r_index[word]["last_doc"]
                if last_doc != doc_id:
                    self.r_index[word]["last_doc"] = doc_id
                    self.r_index[word]["words"].append(doc_id-last_doc)
            else:
                self.r_index[word] = {}
                self.r_index[word]["words"] = [doc_id]
                self.r_index[word]["jump_table"] = {}
                self.r_index[word]["last_doc"] = doc_id


    def encode_it(self):
        for word, word_struct in self.r_index.iteritems():
            word_struct["words"] = vb.encode(word_struct["words"])


    