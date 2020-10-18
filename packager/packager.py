import os
import json

class Packager():
	"""The dolphin packager can create a boilerplate for developing a deployment
	for your cloud native applications. 
	"""

	@classmethod
	def create_package(self, name):
		"""Creates boilerplate for dolphin deployment.
		"""

		instruction_template = {
			"settings": {
				"mode":"kubectl",
				"varpath":""
			},
			"meta": {
				"name":""
			},
			"blocks": [
				{
					"type":"shell",
					"cmd":"echo \"Hello dolphin!\nVersion: %version%\""
				}
			],
			"tests": [
			]
		}

		vars_template = {"version":"beta-3"}
		instruction_template["meta"]["name"] = name
		instruction_template["settings"]["varpath"] = "./"+ name +"/data/"
		
		os.popen("mkdir -p "+ name +"/data").read()
		os.chdir(name)
		print(os.getcwd())

		with open("instructions.json", "w+") as instruction_template_file:
			json.dump(instruction_template, instruction_template_file, indent=4)

		os.chdir("data")

		with open("vars.json", "w+") as vars_template_file:
			json.dump(vars_template, vars_template_file)
