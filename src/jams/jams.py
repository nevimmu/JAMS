import sys
import os
import time
import argparse
import questionary
from .settings import __version__, CONF_DIR
from .dbus_helper import get_players, find_player
from .db_helper import DbHelper

def get_args():
	'''
	Parses the CLI arguments and returns them.
	'''

	parser = argparse.ArgumentParser(description='JAMS Auto-Mute Sometimes')
	parser.add_argument('-s', '--setup', action='store_true', help='Setup JAMS')
	parser.add_argument('-v', '--version', action='store_true', help='JAMS version')

	return parser.parse_args()

def parse_arguments(args, db):
	'''
	Parses the CLI arguments and acts on them.
	'''

	if args.version:
		print(f'JAMS v{__version__}')
		sys.exit(0)

	if args.setup:
		setup(db)
		sys.exit(0)

def setup(db: DbHelper):
	'''
	Sets up the JAMS configuration.
	'''
	# Get a list of all available players
	players = get_players()

	# Music source selection
	music_choice = questionary.select(
		'Choose your music source:',
		choices=players
	).ask()

	# Create a new list of players without the selected music source
	browser_choices = [player for player in players if player != music_choice]

	# Browser source selection
	browser_choice = questionary.select(
		'Choose your browser:',
		choices=browser_choices
	).ask()

	# Save the user's choices to the config file
	db.set('music', music_choice)
	db.set('browser', browser_choice)


def loop(db: DbHelper):
	'''
	The main loop of the application.
	'''
	db.set('was_playing', False)

	while True:
		# Get the music and browser players from the config file
		music = db.get('music')
		browser = db.get('browser')

		# Find the music and browser players
		music_player = find_player(music)
		browser_player = find_player(browser)

		# If the music and browser players are both playing, pause the music player
		if music_player.is_playing() and browser_player.is_playing():
			music_player.pause()
			db.set('was_playing', True)

		# If the browser player is not playing and the music player was playing, play the music player
		if not browser_player.is_playing() and db.get('was_playing'):
			music_player.play()
			db.set('was_playing', False)

		time.sleep(.5)

def main():
	os.makedirs(CONF_DIR, exist_ok=True)
	db = DbHelper()

	args = get_args()
	parse_arguments(args, db)

	loop(db)