# qqdm

A lightweight, fast and pretty progress bar for Python

## Demo
<img src="https://github.com/KimythAnly/qqdm/blob/main/demo.gif" width="768"/>

## Installation
```
pip install qqdm
```

## Usage
The following is a simple example.
```python
import time
import random
from qqdm import qqdm, format_str

tw = qqdm(range(10), desc=format_str('bold', 'Description'))

for i in tw:
  loss = random.random()
  acc = random.random()
  tw.set_infos({
    'loss': f'{loss:.4f}',
    'acc': f'{acc:.4f}',
  })
  time.sleep(0.5)
```

For the demo gif shown above, you may refer to `tests/test.py`.
