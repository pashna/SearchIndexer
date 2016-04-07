# coding: utf-8

class Optimizer():

    def __init__(self, encoder):
        self.encoder = encoder


    def create_jump_table(self, r_index, jump_step=2, count_of_step=None):
        """
        Function convert list of documents_id to list of delta. After it builds jump_table
        :param r_index:
        :param jump_step:
        """

        for word, word_struct in r_index.iteritems():
            doc_list = word_struct["docs"]
            prev_doc_id = doc_list[0]
            word_struct["jump_table"] = {"jump_step": jump_step,
                                         #"jump_index": [],
                                         "jump_values": []
                                         }

            for i in range(1, len(doc_list)):
                if i%jump_step == 0:
                    word_struct["jump_table"]["jump_values"].append(doc_list[i])

                delta = doc_list[i] - prev_doc_id
                prev_doc_id = doc_list[i]
                doc_list[i] = delta


            word_struct["max_doc_id"] = prev_doc_id

        return r_index


    def encode_it(self, r_index):
        for word, word_struct in r_index.iteritems():
            word_struct["docs"] = self.encoder.encode(word_struct["docs"])