import sys
import os
import time
import argparse
import questionary
from .settings import __version__, CONF_DIR
from .dbus_helper import DbusHelper, get_players, find_player
from .db_helper import DbHelper

def get_args():
	'''Get the arguments'''

	parser = argparse.ArgumentParser(description='JAMS Auto-Mute Sometimes')
	parser.add_argument('-s', '--setup', action='store_true', help='Setup JAMS')
	parser.add_argument('-v', '--version', action='store_true', help='JAMS version')

	return parser.parse_args()

def parse_arguments(args, db):
	'''Parse the arguments'''

	if args.version:
		print(f'JAMS v{__version__}')
		sys.exit(0)

	if args.setup:
		setup(db)
		sys.exit(0)

def setup(db: DbHelper):
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

	# Save choices to json file
	db.set('music', music_choice)
	db.set('browser', browser_choice)


def loop(db: DbHelper):
	'''Main loop'''
	db.set('was_playing', False)
	while True:
		music = db.get('music')
		browser = db.get('browser')

		music_player = find_player(music)
		browser_player = find_player(browser)

		if music_player.is_playing() and browser_player.is_playing():
			music_player.pause()
			db.set('was_playing', True)

		if not browser_player.is_playing() and db.get('was_playing'):
			music_player.play()
			db.set('was_playing', False)

		time.sleep(1)

def main():
	os.makedirs(CONF_DIR, exist_ok=True)
	db = DbHelper()

	args = get_args()
	parse_arguments(args, db)

	loop(db)