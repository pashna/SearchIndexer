#!/usr/bin/env python
# coding: utf-8
from Engine.VarByteEncoder import VarByteEncoder
from Engine.Simple9 import Simple9
from Engine.Optimizer import Optimizer
from utils.utils import load_obj
from utils.utils import save_obj
from utils.utils import print_error
from indexing import COUNT_OF_FILES
import time

if __name__ == "__main__":
    start_time = time.time()
    for i in range(COUNT_OF_FILES):
        r_index = load_obj("indexer_"+str(i))
        """
        if r_index.has_key("аркадий"):
            print len(r_index["аркадий"]["docs"])

            optimizer = Optimizer(VarByteEncoder())
            r_index = optimizer.create_jump_table(r_index=r_index, jump_step=300)
            optimizer.encode_it(r_index)

            vbe = VarByteEncoder()
            docs = vbe.decode(r_index["аркадий"]["docs"])
            print len(docs)

        """
        if r_index["encoding"]=="varbyte":
            optimizer = Optimizer(VarByteEncoder())
        else:
            optimizer = Optimizer(Simple9())

        r_index = optimizer.create_jump_table(r_index=r_index, jump_step=300)
        optimizer.encode_it(r_index)
        save_obj(r_index, "optimized_index_"+str(i))
        #"""
    print("--- %s seconds ---" % (time.time() - start_time))