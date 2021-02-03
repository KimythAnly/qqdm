import sys
import shutil
import re
import time
from addict import Dict

symbols = Dict({
        'prev_line': '\033[F',
        'clear_line': '\033[K',
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'yellow': '\033[93m',
        'magenta': '\033[95m',
        'grey' : '\033[90m',
        'black' : '\033[90m',
        'default' : '\033[99m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    })

def fill(msg, token=' ', maxcols=None, align='<'):
    if maxcols is None:
        maxcols = shutil.get_terminal_size()[0]
    exp = maxcols - len_ANSI(msg)
    if align == '<':
        return f'{msg}{token*exp}'
    elif align == '^':
        return f'{token * (exp//2)}{msg}{token * (exp - exp//2)}'
    elif align == '>':
        return f'{token*exp}{msg}'
    else:
        return f'{msg}{token*exp}'

def format_time(t):
    return time.strftime("%H:%M:%S", time.gmtime(t))

def format_str(fmt, s, end=None):
    if end is None:
        end = symbols.end
    if isinstance(fmt, list):
        return ''.join([symbols[f] for f in fmt]) + str(s) + end
    return symbols[fmt] + str(s) + end

# =========================================================
#  Source: https://stackoverflow.com/questions/2186919
#  Author: John Machin
# =========================================================
strip_ANSI_escape_sequences_sub = re.compile(r"""
    \x1b     # literal ESC
    \[       # literal [
    [;\d]*   # zero or more digits or semicolons
    [A-Za-z] # a letter
    """, re.VERBOSE).sub
def strip_ANSI_escape_sequences(s):
    return strip_ANSI_escape_sequences_sub("", s)
# =========================================================

def len_ANSI(msg):
    return len(strip_ANSI_escape_sequences(msg))

class qqdm():
    def __init__(self,
        iterable,
        dynamic_ncols=True,
        desc='',
        total=None,
        **kwargs
    ):
        self.fp = sys.stderr
        self.iterable = iterable
        self.iter = iter(self.iterable)
        self.dynamic_ncols = dynamic_ncols
        self.desc = desc
        self.total = total or len(self.iterable)
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
        self.ncols = 20
        self.temp_ncols = 0
        self.msg = ''
        self._msg = ''
        self.updated_time = 0
        self.set_bar(0)
        self.set_info('Iters', f'{self.counter}/{format_str("yellow",len(self))}')
        self.set_info('Elapsed Time', '-')
        self.set_info('Speed', '-')
        self.update()


    def set_ctrls_by_dict(self, dct):
        for k, v in dct.items():
            self.set_ctrls(k, v)

    def set_ctrls(self, k, v):
        self.ctrls[k] = v

    def __len__(self):
        return self.total

    def __iter__(self):
        # for i in self.tqdm:
            # yield i
        self.start_time = time.time()
        return self

    def get_ncols(self):
        if self.dynamic_ncols:
            return shutil.get_terminal_size()[0]
        else:
            return self.ncols

    def set_infos(self, dct, ordered_key=None):
        if ordered_key:
            for key in ordered_key:
                self.set_info(key, dct[key])
        else:
            for key, value in dct.items():
                self.set_info(key, value)

    def set_info(self, key, val):
        if key not in self.info_dict:
            self.ordered_key.append(key)
        self.info_dict[key] = str(val)

    # ■█▶
    def set_bar(self, persent, color='white', element='█'):
        if self.desc:
            msg = f'{self.desc} {persent*100: >5.1f}%'
        else:
            msg = f'{persent*100: >5.1f}%'
        ncols = self.get_ncols()
        # The 3 stands for the length of the template message (1 for space, 2 for ||).
        bar_ncols = ncols - 3 - len_ANSI(msg)
        bar = format_str(color, element) * int(persent * bar_ncols)
        bar = fill(bar, ' ', bar_ncols)
        # self.bar = f'{persent*100: >5.1f}% |{bar}|'
        self.bar = f'{msg} |{bar}|'

    def _set_info(self):

        elapsed = time.time() - self.start_time
        persent = self.counter / len(self)
        remaining = elapsed * (1 / persent - 1) if self.counter != 0 else 0

        self.set_bar(persent)

        _elapsed = format_time(elapsed)
        _remaining = format_time(remaining)

        self.set_info('Iters', f'{self.counter}/{format_str("yellow",len(self))}')
        if self.counter != 0:
            self.set_info('Elapsed Time', f'{_elapsed}<{format_str("yellow", _remaining)}')
        else:
            self.set_info('Elapsed Time', f'{_elapsed}<{format_str("yellow", "?")}')
        self.set_info('Speed', f'{self.counter / elapsed:.2f}it/s')

    def __next__(self):

        try:
            ret = next(self.iter)
            if time.time() - self.updated_time > 0.2:
                self._set_info()
                self.update()
            self.counter += 1
            return ret
        except:
            self._set_info()
            self.update()
            self.fp.write('\n')
            self.fp.flush()
            raise StopIteration

    def _add_str(self, msg):
        return msg

    def _add_list(self, msg):
        return ''.join([str(s) for s in msg])

    def _add_dict(self, msg, kv_format):
        if kv_format is None:
            kv_format = self.default_kv_format
        ret = []
        for k, v in msg.items():
            ret.append(kv_format.format(key=k, value=v))
        ret = '\n'.join(ret)
        return ret

    def add(self, msg, kv_format=None):
        if isinstance(msg, str):
            _msg = self._add_str(msg)
        elif isinstance(msg, list):
            _msg = self._add_list(msg)
        elif isinstance(msg, dict):
            _msg = self._add_dict(msg, kv_format)
        else:
            _msg = str(msg)
        # update self.msg
        if self.msg and _msg:
            self.msg = '\n'.join([self.msg, _msg])
        elif _msg:
            self.msg = _msg
        else:
            self.msg = ''

    def update(self, *args):
        # flush the msg
        ncols = self.get_ncols()
        prefix_upper_border = fill('', '')
        values = []
        lengths = []
        indexes = []
        for key in self.ordered_key:
            value = self.info_dict[key]
            values.append(value)
            lengths.append(max(len_ANSI(key), len_ANSI(value)) + 2)
        aggr_length = 0
        index = 0
        for length in lengths:
            aggr_length = aggr_length + length
            if aggr_length >= ncols:
                index = index + 1
                aggr_length = length
            indexes.append(index)
        prefix = [[] for i in range((index+1) * 2)]
        for key, value, length, index in zip(self.ordered_key, values, lengths, indexes):
            prefix[index*2].append(
                fill(
                    format_str(self.ctrls['key'], key),
                    ' ',
                    maxcols=length,
                    align='^',
                )
            )
            prefix[index*2 + 1].append(
                fill(
                    format_str(
                        self.ctrls['value'], value),
                        ' ',
                        maxcols=length,
                        align='^',
                    )
            )
        prefix = [
            ''.join(line_list) for line_list in prefix
        ]
        prefix = '\n'.join(prefix)
        lines = [
            prefix_upper_border,
            prefix,
            self.msg,
            self.bar,
        ]
        lines = '\n'.join(lines)
        if self._msg:
            n_line = self._msg.count('\n')
        else:
            n_line = 0
        # n_line = n_line * (self.temp_ncols+ncols+1) // ncols -1
        _msg_filled = []
        for m in lines.split('\n'):
            if m:
                _msg_filled.append(fill(m, ' '))
        _msg = '\n'.join(_msg_filled)
        self._msg = n_line * (symbols.clear_line+symbols.prev_line) + _msg
        # if self._msg:
            # self._msg = f'{self._msg}\n{self.bar}'
        self.fp.write(self._msg)
        self.fp.flush()
        self.msg = ''
        self.temp_ncols = ncols
        self.updated_time = time.time()

__all__ = [
    'qqdm',
    'format_str'
]
