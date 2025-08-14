import dbus

class DbusHelper:
	'''This class interact with dbus MediaPlayer2 interface'''

	_name = None
	_service = None
	_player = None
	_interface = None
	_info = {}
	_bus = dbus.SessionBus()
	
	def __init__(self, service):
		self._service = service
		self._player = self._bus.get_object(self._service, '/org/mpris/MediaPlayer2')
		self._interface = dbus.Interface(self._player, dbus_interface='org.freedesktop.DBus.Properties')

	def _get_metadata(self):
		metadata = self._interface.GetAll('org.mpris.MediaPlayer2.Player')
		for key, value in metadata.items():
			if isinstance(value, dict):
				for subk, subv in value.items():
					self._info[subk] = subv
			self._info[key] = value

	def is_playing(self):
		self._get_metadata()
		return self._info['PlaybackStatus'] == 'Playing'

	def get_title(self):
		self._get_metadata()
		return self._info['xesam:title']
	

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


def get_players() -> dict:
	'''Get a dict of players'''
	_players = {}
	for session in dbus.SessionBus().list_names():
		if 'org.mpris.MediaPlayer2' in session:
			if 'instance' in session:
				_players[str(session.split('.')[-2])] = session
			else:
				_players[str(session.split('.')[-1])] = session

	return _players

def find_player(name) -> DbusHelper:
	'''Find a player from it's name'''
	players = get_players()

	return DbusHelper(players[name])
