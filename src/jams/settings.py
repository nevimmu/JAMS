import os

__version__ = '0.1.1'

HOME = os.getenv('HOME') or os.getenv('USERPROFILE') or os.path.expanduser('~')
XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME') or os.path.join(HOME, '.config')

CONF_DIR = os.path.join(XDG_CONF_DIR, 'jams')