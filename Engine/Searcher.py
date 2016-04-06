# coding: utf-8

from Engine.VarByteEncoder import VarByteEncoder as vb

class Searcher():

    def __init__(self, r_index):
        self.r_index = r_index


    def and_words(self, w1, w2):
        w1_struct = self.r_index[w1]
        w2_struct = self.r_index[w2]

        #пусть docs_1 будет самым коротким из двух
        if len(w1_struct["docs"]) > len(w2_struct["docs"]):
            #jump_table_1 = w2_struct["jump_table"]
            jump_table_2 = w1_struct["jump_table"]
            docs_1 = w2_struct["docs"]
            docs_2 = w1_struct["docs"]
        else:
            #jump_table_1 = w1_struct["jump_table"]
            jump_table_2 = w2_struct["jump_table"]
            docs_1 = w1_struct["docs"]
            docs_2 = w2_struct["docs"]

        # Декодируем
        docs_1 = vb.decode(docs_1)
        docs_2 = vb.decode(docs_2)

        result_docs = []
        prev_doc = 0
        for i in range(len(docs_1)):
            doc_id = docs_1[i] + prev_doc
            prev_doc = doc_id

            if (self._find_doc(doc_id, docs_2, jump_table_2)):
                result_docs.append(doc_id)

        return result_docs


    def _find_doc(self, doc_id, docs, jump_table):
        """
        Ищем doc_id в docs с помощью jumb_table
        :param doc_id:
        :param docs:
        :param jump_table:
        """
        jump_step = jump_table["jump_step"]
        step_count = doc_id/jump_step

        left_border_value = step_count*jump_step
        right_border_value = (step_count+1)*jump_step

        if left_border_value == 0:
            # может быть в первом сегменте
            left_border_index = 0
        elif jump_table.has_key(left_border_value):
            #
            left_border_index = jump_table[left_border_value]
        else:
            return False

        if jump_table.has_key(right_border_value):
            right_border_index = jump_table[right_border_value]
        else:
            # Последний сегмент
            right_border_index = len(docs)

        prev_doc_id = left_border_value - docs[left_border_index]# это нужно, чтобы работал цикл for
        for i in range(left_border_index, right_border_index):
            real_doc_id = docs[i] + prev_doc_id
            prev_doc_id = real_doc_id
            if doc_id == real_doc_id:
                return True

        return False




