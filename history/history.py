import json

class History():

	@classmethod
	def export(self, path, name, history_data):
		"""Stores entry to history...
		"""

		history_json = json.load(open(path, "r"))
		history_json[name] = history_data
		with open(path, "w+") as history_json_file:
			json.dump(history_json, history_json_file, indent=6)

	@classmethod
	def show(self, path):
		"""Shows history data...
		"""

		history_json = json.load(open(path, "r"))

		for epoch_key in history_json:
			print("ID: "+ history_json[epoch_key]["id"])
			print("Time deployed: "+ history_json[epoch_key]["time"])
			print("Result status: "+ history_json[epoch_key]["status"])

			if "meta" in history_json[epoch_key].keys():
				print("User defined labels:")
				for label in history_json[epoch_key]["meta"].keys():
					print(label +": "+ history_json[epoch_key]["meta"][label])