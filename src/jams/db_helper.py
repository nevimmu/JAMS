import os
import json
from .settings import CONF_DIR

class DbHelper():
	'''Manage JAMS database'''

	def __init__(self):
		self._conf_name = 'jams.json'
		self._conf_file = os.path.join(CONF_DIR, self._conf_name)

		if not os.path.isfile(self._conf_file):
			self.create_config()

	def create_config(self):
		config = {
			'music': '',
			'browser': '',
			'was_playing': False,
		}

		self._write_config(config)

	def _read_config(self):
		with open(self._conf_file, 'r') as f:
			return json.load(f)

	def _write_config(self, config):
		with open(self._conf_file, 'w') as f:
			json.dump(config, f, indent='\t', separators=(',', ':'))

	def get(self, source):
		data = self._read_config()
		return data[source]

	def set(self, source, value):
		data = self._read_config()
		data[source] = value
		self._write_config(data)