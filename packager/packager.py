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
				"varpath":"data/"
			},
			"meta": {
				"name":""
			},
			"blocks": [
				{
					"type":"kubectl.shell",
					"cmd":"echo \"Hello dolphin!\nVersion: %version%\""
				}
			],
			"tests": [
				{
					"script":"echo \"It works!\"",
					"expected_result":"It works!\n"
				}
			]
		}

		vars_template = {"version":"beta-4"}
		instruction_template["meta"]["name"] = name

		os.popen("mkdir -p "+ name +"/data").read()
		os.chdir(name)
		print(os.getcwd())

		with open("instructions.json", "w+") as instruction_template_file:
			json.dump(instruction_template, instruction_template_file, indent=4)

		os.chdir("data")

		with open("vars.json", "w+") as vars_template_file:
			json.dump(vars_template, vars_template_file)
