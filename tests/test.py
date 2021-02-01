import time
import random
from qqdm import qqdm, format_str


start = time.time()

for ep in range(2):
    tw = qqdm(range(100), desc=format_str('blue', f'asdadsfd'))
    time.sleep(1)
    for i in tw:
        tw.set_infos({
            'loss': f'{random.random():.4f}',
            'acc': f'{random.random():.4f}',
        })
        time.sleep(.01)
    print('Done')
    time.sleep(2)

