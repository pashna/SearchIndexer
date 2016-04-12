#!/usr/bin/env python
# coding: utf-8
from Engine.VarByteEncoder import VarByteEncoder
from Engine.Simple9 import Simple9
from Engine.Optimizer import Optimizer
from utils.utils import load_obj
from utils.utils import save_obj
from utils.utils import print_error

if __name__ == "__main__":
    optimizer = Optimizer(Simple9())
    #full_r_index = load_obj("indexer")
    r_index = load_obj("indexer")
    #for letter, r_index in full_r_index.iteritems():
    r_index = optimizer.create_jump_table(r_index=r_index, jump_step=300)
    optimizer.encode_it(r_index)
    save_obj(r_index, "optimized_index")
