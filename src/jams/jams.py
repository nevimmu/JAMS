import sys
import os
import argparse
from .settings import __version__, CONF_DIR
from .dbus_helper import DbusHelper, get_players

def get_args():
	'''Get the arguments'''

	parser = argparse.ArgumentParser(description='JAMS Auto-Mute Sometimes')
	parser.add_argument('-s', '--setup', action='store_true', help='Setup JAMS')
	parser.add_argument('-v', '--version', action='store_true', help='JAMS version')

	return parser.parse_args()

def parse_arguments(args):
	'''Parse the arguments'''

	if args.version:
		print(f'JAMS v{__version__}')
		sys.exit(0)

	if args.setup:
		print('Setup')
		sys.exit(0)

def loop():
	'''Main loop'''
	players = get_players()
	for p in players:
		print(p)

def main():
	os.makedirs(CONF_DIR, exist_ok=True)

	args = get_args()
	parse_arguments(args)

	loop()