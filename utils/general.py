def argmin(d, key):
    min_val = min(d, key=key)
    return [k for k,val in enumerate(d) if val[0] == min_val[0] and val[1]==min_val[1]][0]