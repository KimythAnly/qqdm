import sys
import shutil
import time

from addict import Dict
from IPython.display import display
from ipywidgets import FloatProgress, HTML, HBox

from .util import symbols, format_time, len_ANSI, fill
from .util import format_str as _format_str
from .core import qqdm as _qqdm

class SuperString(str):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return str(self.s)

class DummyBar(HBox):
    def __init__(self, persent=0.0, description=None):
        self.description = description
        # Init
        self.prefix = HTML()
        self.update()
        super().__init__(children=[self.prefix])
        
    def update(self, description=None, **kwrags):
        if description:
            self.description = description
        if self.description:
            self.prefix.value = self.description

    def set_bar_style(self, *args, **kwargs):
        pass

class IpythonBar(HBox):
    def __init__(self, persent=0.0, description=None):
        self.description = description
        self.persent = persent
        # Init
        self.prefix = HTML()
        self.bar = FloatProgress()
        self.update()
        super().__init__(children=[self.prefix, self.bar])

    def update(self, persent=None, description=None):
        if description:
            self.description = description
        if persent:
            self.persent = persent
        if self.description:
            prefix = f'{self.description}  {self.persent*100: >5.1f}%'
        else:
            prefix = f'{self.persent*100: >5.1f}%'
        self.prefix.value = prefix
        self.bar.value = self.persent*100
    
    def set_bar_style(self, style):
        self.bar.bar_style = style


def format_str(fmt, s, end=None):
    return SuperString(_format_str(fmt, s, end))


class qqdm(_qqdm):
    def __init__(self,
        iterable,
        dynamic_ncols=True,
        desc='',
        total=None,
        **kwargs
    ):
        # self.fp = sys.stderr
        self.fp = display(None, display_id=True)
        self.iterable = iterable
        self.iter = iter(self.iterable)
        self.dynamic_ncols = dynamic_ncols
        self.desc = desc
        if total:
            self.total = total
        else:
            try:
                self.total = len(self.iterable)
            except:
                self.total = None
        # Reset
        self.reset()

    def reset(self):
        self.default_kv_format = format_str(['blue'], '{key}: ') + '{value}'
        self.ctrls = Dict({
            'key': ['bold'],
            'value': 'default',
            'default': 'default',
            'end': 'end'
        })
        self.info_dict = {}
        self.ordered_key = []
        self.counter = 0
        self.ncols = 60
        self.temp_ncols = 0
        self.msg = ''
        self._msg = ''
        self.updated_time = 0
        if hasattr(self, '_bar'):
            self._bar.close()
        if self.total:
            self.set_info('Iters', f'{self.counter}/{format_str("yellow",self.total)}')
            self.bar = IpythonBar(persent=0.0, description=self.desc) # FloatProgress(description=f'{0: >5.1f}%')
        else:
            self.set_info('Iters', self.counter)
            self.bar = DummyBar(description=self.desc)
        display(self.bar)
        self.set_info('Elapsed Time', '-')
        self.set_info('Speed', '-')
        self.update()

    def __iter__(self):
        try:
            self.start_time = time.time()
            # return self
            for i in self.iter:
                yield i
                self.counter += 1
                if time.time() - self.updated_time > 0.2:
                    self._set_info()
                    self.update()
            self._set_info()
            self.update()
            self.bar.set_bar_style('success')
        except:
            self.bar.set_bar_style('danger')

    def set_bar(self, persent, color='white', element='█'):
        self.bar.update(persent)

    def write_flush(self, message):
        self.fp.update(SuperString(self._msg))


__all__ = [
    'qqdm',
    'format_str'
]
