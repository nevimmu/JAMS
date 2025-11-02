import os
import json
from .settings import CONF_DIR

class DbHelper():
	'''
	A helper class to manage the JAMS database stored in a JSON file.
	'''

	def __init__(self):
		self._conf_name = 'jams.json'
		self._conf_file = os.path.join(CONF_DIR, self._conf_name)
		self._template_file = os.path.join(CONF_DIR, 'jams.json.template')

		# If the config file doesn't exist, create it.
		if not os.path.isfile(self._conf_file):
			self.create_config()
		else:
			# Ensure the config file is writable (fix permissions if needed)
			self._ensure_writable()

	def create_config(self):
		# Check if there's a template file from home-manager
		if os.path.isfile(self._template_file):
			# Read the template and create a writable copy
			import json
			with open(self._template_file, 'r') as f:
				config = json.load(f)
			self._write_config(config)
		else:
			# Create a default config
			config = {
				'music': '',
				'browser': '',
				'was_playing': False,
			}
			self._write_config(config)

	def _ensure_writable(self):
		'''
		Ensures the config file is writable by setting proper permissions.
		'''
		if os.path.isfile(self._conf_file):
			import stat
			# Set read and write permissions for the owner
			os.chmod(self._conf_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

	def _read_config(self):
		'''
		Reads the config file and returns the data as a dictionary.
		'''
		with open(self._conf_file, 'r') as f:
			return json.load(f)

	def _write_config(self, config):
		'''
		Writes the given config dictionary to the config file.
		'''
		with open(self._conf_file, 'w') as f:
			json.dump(config, f, indent='\t', separators=(',', ':'))

	def get(self, source):
		'''
		Retrieves a value from the config file.
		'''
		data = self._read_config()
		return data[source]

	def set(self, source, value):
		'''
		Sets a value in the config file.
		'''
		data = self._read_config()
		data[source] = value
		self._write_config(data)