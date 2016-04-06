# coding: utf-8
from VarByteEncoder import VarByteEncoder as vb

class Optimizer():

    @staticmethod
    def create_jump_table(r_index, jump_step=2, count_of_step=None):
        """
        Функция переводит массив документов в массив приращений(дельт), и строит jump_table
        :param r_index:
        :param jump_step:
        """

        for word, word_struct in r_index.iteritems():
            doc_list = word_struct["docs"]
            prev_doc_id = doc_list[0]
            word_struct["jump_table"] = {"jump_step": jump_step}

            for i in range(1, len(doc_list)):
                delta = doc_list[i] - prev_doc_id
                prev_doc_id = doc_list[i]
                doc_list[i] = delta

                if i%jump_step == 0:
                    word_struct["jump_table"][i] = prev_doc_id

            word_struct["max_doc_id"] = prev_doc_id

        return r_index


    @staticmethod
    def encode_it(r_index):
        for word, word_struct in r_index.iteritems():
            word_struct["docs"] = vb.encode(word_struct["docs"])
            decoded = vb.decode(word_struct["docs"])