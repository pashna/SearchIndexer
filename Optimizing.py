from Engine.Optimizer import Optimizer
from utils.utils import load_obj
from utils.utils import save_obj

if __name__ == "__main__":
    optimizer = Optimizer()
    r_index = load_obj("indexer")
    r_index = optimizer.create_jump_table(r_index=r_index, jump_step=150)
    optimizer.encode_it(r_index)
    save_obj(r_index, "optimized_index")