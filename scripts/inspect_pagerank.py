import pickle
from pathlib import Path
p = Path('data/pr/pagerank.pkl')
try:
    d = pickle.load(open(p,'rb'))
    print(type(d), len(d))
    for i, (k, v) in enumerate(d.items()):
        if i >= 10:
            break
        print(k, v)
except Exception as e:
    print('ERROR', e)
