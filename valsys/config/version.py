def read_config():
    with open("CONFIG") as v:
        ls = v.read().splitlines()
        lds = {}
        for l in ls:
            k, v = l.split('=')
            lds[k] = v
    return lds


cfg = read_config()

VERSION = cfg['VERSION']
NAME = cfg['NAME']
