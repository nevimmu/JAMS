import sys
import os
import argparse
import questionary
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
		setup()
		sys.exit(0)

def setup():
	players = get_players()
	music_choice = questionary.select(
		'Choose your music source:',
		choices=players
	).ask()

	# Create a new list of players without music_choice
	browser_choices = [player for player in players if player != music_choice]

	browser_choice = questionary.select(
		'Choose your browser:',
		choices=browser_choices
	).ask()

	print(f'Music: {players[music_choice]}')
	print(f'Browser: {players[browser_choice]}')


def loop():
	'''Main loop'''
	pass

def main():
	os.makedirs(CONF_DIR, exist_ok=True)

	args = get_args()
	parse_arguments(args)

	loop()