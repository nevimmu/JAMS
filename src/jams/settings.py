import os

__version__ = '0.1.0'

HOME = os.getenv('HOME', os.getenv('USERPROFILE'))
XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.join(HOME, '.config'))

CONF_DIR = os.path.join(XDG_CONF_DIR, 'jams')