import json

class Messages():
	"""All custom exception messages, usage info, and application info
	messages are stored in JSON files within the infod root directory.
	Each of these are loaded here and can be accessed using the getters
	provided with the object.
	"""

	@classmethod
	def get_exception_msg(self, code):
		"""Looks up exception message by code in the EXCEPTIONS.json object
		and returns the data.
		"""

		messages = json.load(open("infod/EXCEPTIONS.json", "r"))
		return messages[code]

	@classmethod
	def get_info_msg(self, code):
		"""Looks up exception message by code in the EXCEPTIONS.json object
		and returns the data.
		"""

		messages = json.load(open("infod/INFO.json", "r"))
		return messages[code]

	@classmethod
	def get_usage_msg(self, code):
		"""Looks up exception message by code in the EXCEPTIONS.json object
		and returns the data.
		"""

		messages = json.load(open("infod/USAGE.json", "r"))
		return messages[code]
