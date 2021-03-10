import time
from qqdm import qqdm
from tqdm import tqdm

def task(fn, r=1000):
    s = time.time()
    for i in fn(range(r)):
        time.sleep(.001)
        pass
    print(f'Fn: {fn}')
    print(f'Using time: {time.time()-s:.5f} sec.')

if __name__ == '__main__':
    task(qqdm)
    task(tqdm)
