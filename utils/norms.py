import numpy as np
def norm_L2(*args):
    args_2 = np.square(args)
    return np.sqrt(args_2.sum())