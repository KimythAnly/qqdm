import time
import shutil
import re

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

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


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
