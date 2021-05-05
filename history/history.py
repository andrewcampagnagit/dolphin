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
	def show(self, path, args=None):
		"""Shows history data...
		"""

		history_json = json.load(open(path, "r"))

		for epoch_key in history_json:
			history_block = []
			history_block.append("ID:"+ history_json[epoch_key]["id"])
			history_block.append("TimeDeployed:"+ history_json[epoch_key]["time"])
			history_block.append("ResultStatus:"+ history_json[epoch_key]["status"])

			if "meta" in history_json[epoch_key].keys():
				for label in history_json[epoch_key]["meta"].keys():
					history_block.append(label +": "+ history_json[epoch_key]["meta"][label])
			
			if args == None:
				print(history_block)

			elif all(arg in history_block for arg in args):
				print(history_block)