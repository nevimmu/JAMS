import dbus
import time
from typing import Dict, Any, Optional

class DbusHelper:
	'''
	Helper class to interact with the DBus MediaPlayer2 interface.
	'''

	_name: Optional[str] = None
	_service: Optional[str] = None
	_player: Optional[Any] = None
	_interface: Optional[Any] = None
	_info: Dict[str, Any] = {}
	_bus = dbus.SessionBus()
	
	def __init__(self, service):
		try:
			self._service = service
			self._player = self._bus.get_object(self._service, '/org/mpris/MediaPlayer2')
			self._interface = dbus.Interface(self._player, dbus_interface='org.freedesktop.DBus.Properties')
		except dbus.exceptions.DBusException as e:
			print(f'DBUS Error: {e}')

	def _get_metadata(self):
		'''
		Gets the metadata from the player and stores it in the _info dictionary.
		'''
		if self._interface is None:
			return
		try:
			metadata = self._interface.GetAll('org.mpris.MediaPlayer2.Player')
			for key, value in metadata.items():
				if isinstance(value, dict):
					for subk, subv in value.items():
						self._info[subk] = subv
				self._info[key] = value
		except dbus.exceptions.DBusException as e:
			print(f'DBUS Error: {e}')

	def is_playing(self) -> bool:
		try:
			self._get_metadata()
			if not self._info:
				return False
			return self._info.get('PlaybackStatus') == 'Playing'
		except (dbus.exceptions.DBusException, KeyError) as e:
			print(f'DBUS Error: {e}')
			return False

	def get_title(self) -> str:
		self._get_metadata()
		return self._info.get('xesam:title', '')
	

	def play(self):
		dbus.Interface(
			self._player,
			dbus_interface='org.mpris.MediaPlayer2.Player'
		).Play()

	def pause(self):
		dbus.Interface(
			self._player,
			dbus_interface='org.mpris.MediaPlayer2.Player'
		).Pause()


def get_players() -> Dict[str, str]:
	'''
	Gets a dictionary of all available players.
	The key is the player name, and the value is the DBus service name.
	'''
	_players: Dict[str, str] = {}
	try:
		bus = dbus.SessionBus()
		names = bus.list_names()
		if names is not None:
			for session in names:
				if 'org.mpris.MediaPlayer2' in session:
					if 'instance' in session:
						_players[str(session.split('.')[-2])] = session
					else:
						_players[str(session.split('.')[-1])] = session
	except dbus.exceptions.DBusException as e:
		print(f'DBUS Error: {e}')

	return _players

def find_player(name: str) -> DbusHelper:
	'''
	Finds a player by its name and returns a DbusHelper object for it.
	If the player is not found, it will keep trying until it is found.
	'''
	while True:
		players = get_players()
		if name in players:
			return DbusHelper(players[name])
		time.sleep(1)
