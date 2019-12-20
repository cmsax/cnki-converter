from os import getenv
from platform import system


def os_type():
    """get os type"""
    sys = system().lower()
    if 'darwin' in sys:
        return 'mac'
    elif 'win' in sys:
        return 'win'
    else:
        return 'linux'


def window_size():
    """get window size"""
    sizes = {'win': 'WIN_APP_WINDOW_SIZE',
             'mac': 'MAC_APP_WINDOW_SIZE', 'linux': 'LINUX_APP_WINDOW_SIZE'}
    return tuple(int(i)
                 for i in getenv(sizes[os_type()], '250, 140').split(', '))
