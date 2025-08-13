import dbus

class DbusHelper:
	'''This class interact with dbus MediaPlayer2 interface'''

	_name = None
	_service = None
	_player = None
	_interface = None
	_bus = dbus.SessionBus()
	
	def __init__(self, service, name):
		self._service = service
		self._name = name
		self._player = self._bus.get_object(self._service, '/org/mpris/MediaPlayer2')
		self._interface = dbus.Interface(self._player, dbus_interface='org.freedesktop.DBus.Properties')

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