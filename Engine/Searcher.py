# coding: utf-8

#from Engine.VarByteEncoder import VarByteEncoder as vb
#from utils.utils import print_error
from indexing import COUNT_OF_FILES
from utils.utils import load_obj, print_error
from Engine.VarByteEncoder import VarByteEncoder
from Engine.Simple9 import Simple9
import mmh3

class Searcher():

    def __init__(self):
        self.r_index = {}#r_index
        self.encoder = None


    def _and_words(self, w1, w2):


        w1_struct = self.get_word_struct(w1)#r_index[w1]
        if w1_struct is None:
            return []

        w2_struct = self.get_word_struct(w2)#r_index[w2]
        if w2_struct is None:
            return []

        # Let docs_1 be smaller than docs_2
        if len(w1_struct["docs"]) > len(w2_struct["docs"]):
            jump_table_2 = w1_struct["jump_table"]
            docs_1 = w2_struct["docs"]
            docs_2 = w1_struct["docs"]
        else:
            jump_table_2 = w2_struct["jump_table"]
            docs_1 = w1_struct["docs"]
            docs_2 = w2_struct["docs"]

        # Decoding
        docs_1 = self.encoder.decode(docs_1)
        docs_2 = self.encoder.decode(docs_2)

        result_docs = []
        prev_doc = 0
        for i in range(len(docs_1)):
            doc_id = docs_1[i] + prev_doc
            prev_doc = doc_id

            if (self._find_doc(doc_id, docs_2, jump_table_2)):
                result_docs.append(doc_id)

        return result_docs


    def get_word_struct(self, w):
        w = w.encode('utf-8')
        __w_hash = mmh3.hash(w) % COUNT_OF_FILES

        if not self.r_index.has_key(__w_hash%COUNT_OF_FILES):
            self.r_index[__w_hash] = load_obj("optimized_index_"+str(__w_hash))

        if self.encoder is None:
            if self.r_index[__w_hash]['encoding'] == 'varbyte':
                self.encoder = VarByteEncoder()
            else:
                self.encoder = Simple9()

        if self.r_index[__w_hash].has_key(w):
            return self.r_index[__w_hash][w]
        else:
            return None

    def and_word_and_docs(self, docs_1, w2):
        w2_struct = self.get_word_struct(w2)#r_index[w]
        if w2_struct is None:
            return []

        jump_table_2 = w2_struct["jump_table"]
        docs_2 = w2_struct["docs"]
        docs_2 = self.encoder.decode(docs_2)

        result_docs = []
        for i in range(len(docs_1)):
            doc_id = docs_1[i]
            if (self._find_doc(doc_id, docs_2, jump_table_2)):
                result_docs.append(doc_id)

        return result_docs


    def _find_doc(self, doc_id, docs, jump_table):
        jump_values = jump_table["jump_values"]
        jump_step = jump_table["jump_step"]
        left_border, right_border, left_value = self._find_interval(jump_values, doc_id, jump_step)

        if right_border == -1 or right_border > len(docs):
            right_border = len(docs)

        if left_value == -1:
            left_value = docs[0]

        prev_doc_id = left_value - docs[left_border]# crutch, but it needs to correct cicle for
        for i in range(left_border, right_border):
            real_doc_id = docs[i] + prev_doc_id
            prev_doc_id = real_doc_id
            if doc_id == real_doc_id:
                return True


    def _find_interval(self, jump_values, value, jump_step):

        result_index = next((jump_values.index(n) for n in jump_values if n > value), len(jump_values))
        if result_index == 0:
            return 0, jump_step, -1
        if result_index < len(jump_values):
            return result_index*jump_step, (result_index+1)*jump_step, jump_values[result_index-1]
        else:
            return result_index*jump_step, -1, jump_values[-1]


    def find_word(self, w):

        w_struct = self.get_word_struct(w)#r_index[w]
        if w_struct is None:
            return []

        docs = w_struct["docs"]
        docs = self.encoder.decode(docs)
        prev_doc = 0
        result_docs = []
        for d in docs:

            real_doc_id = prev_doc + d
            prev_doc = real_doc_id
            result_docs.append(real_doc_id)

        return result_docs


    def and_word_list(self, words):

        w1 = words[0]
        for w in words[1:]:
            w2 = w
            w1 = self.and_(w1, w2)

        return w1



    def and_(self, w1, w2):
        """
        AND
        :param w1: [doc_1, doc_2, ...] or STR
        :param w2: [doc_1, doc_2, ...] or STR
        """
        if not isinstance(w1, list) and not isinstance(w2, list):
            return self._and_words(w1, w2)

        if isinstance(w1, list) and not isinstance(w2, list):
            return self.and_word_and_docs(w1, w2)

        if not isinstance(w1, list) and isinstance(w2, list):
            return self.and_word_and_docs(w2, w1)

        if isinstance(w1, list) and isinstance(w2, list):
            return sorted(list(set(w1) & set(w2)))




    def or_(self, w1, w2):
        """
        OR
        :param w1: [doc_1, doc_2, ...] or STR
        :param w2: [doc_1, doc_2, ...] or STR
        """
        if not isinstance(w1, list) and not isinstance(w2, list):
            docs_1 = self.find_word(w1)
            docs_2 = self.find_word(w2)

        if isinstance(w1, list) and not isinstance(w2, list):
            docs_1 = w1
            docs_2 = self.find_word(w2)

        if not isinstance(w1, list) and isinstance(w2, list):
            docs_1 = self.find_word(w1)
            docs_2 = w1

        if isinstance(w1, list) and isinstance(w2, list):
            docs_1 = w1
            docs_2 = w2

        docs_1.extend(docs_2)

        return sorted(list(set(docs_1)))



    def and_not(self, w1, w2):
        """
        w1 and not w2
        :param w1:
        :param w2:
        """
        # Сделаю пока лениво
        if not isinstance(w1, list) and not isinstance(w2, list):
            docs_1 = self.find_word(w1)
            docs_2 = self.find_word(w2)

        if isinstance(w1, list) and not isinstance(w2, list):
            docs_1 = w1
            docs_2 = self.find_word(w2)

        if not isinstance(w1, list) and isinstance(w2, list):
            docs_1 = self.find_word(w1)
            docs_2 = w1

        if isinstance(w1, list) and isinstance(w2, list):
            docs_1 = w1
            docs_2 = w2


        return sorted(list(set(docs_1)-set(docs_2)))


    def not_and(self, w1, w2):
        """
        not w1 and w2
        :param w1:
        :param w2:
        """
        return self.and_not(w2, w1)