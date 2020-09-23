"""
Dolphin - Cloud deployment and packaging framework.

Version: BETA 2.0.0

Summary:
Dolphin aims to ease the multistage cloud application deployment process
by creating instruction blocks for each part of the process. What makes this
process different is the robust set of functionality that dolphin features
in its templates. You can specify instruction blocks to store
variables from deployed resources along the way dynamically. Another great 
feature is the ability to impose a wait instruction on a resource; this halts 
all operations from that point in the deployment until a specific condition is
met, like a pod in Running status. These features come with our of the box
BlockProcessors, but you can write your own processor easily.

Learn more at: <URL_TO_REFS>

Version notes:
This version is a beta and does not come with complete functionality and could
contain bugs that negatively impact deployments to production environments.

(C) 2020 Server Center - Cloud Development Software LLC. 
"""

import sys
import os
import json
import logging
import requests
from instructionparser import InstructionParser
from tools.exceptions import *

def cleanup():
	"""Cleans up any temp files and folders used for deployment.
	"""

	if os.path.exists("tmp.yaml"):
		os.popen("rm tmp.yaml")

	if os.path.exists(".dolphin_last_out.log"):
		os.popen("rm .dolphin_last_out.log")

def download_instructions():
	"""Downloads instruction file from either file or [GET] request.
	"""

	instruction_blocks = None

	if sys.argv[2] in ["--GET", "-G"]:
		instruction_blocks = json.loads(requests.get(sys.argv[3]).content)

	elif sys.argv[2] in ["--file", "-f"]:
		instruction_blocks = json.load(open(sys.argv[3]))

	else:
		raise Exception(INSTRUCTION_DL_FUNC_NOTFOUND)

	return instruction_blocks

def deploy():
	"""Loads a new parser from mode configuration in instruction block file.
	Each block is then is processed in the parseblock(<block>) method provided
	by the parser. To understand what this method does in depth see the
	comments in the InstructionParser class for the parseblock() method.
	"""

	try:
		instruction_blocks = download_instructions()
	except Exception as e:
		logging.error(e)
		exit()

	if "preload" in sys.argv:
		try:
			var_data = requests.get(sys.argv[-1]).content
			var_path = instruction_blocks["settings"]["varpath"] +"/vars.json"

			with open(var_path, "w+") as vars_file:
				vars_file.write(var_data.decode("utf8"))

		except Exception as e:
			logging.error(e)
			exit()

	parser = InstructionParser(instruction_blocks["settings"]["mode"],
							   instruction_blocks["settings"]["varpath"])

	for block in instruction_blocks["blocks"]:
		parser.parseblock(block)

if __name__ == "__main__":

	if sys.argv[1] in ["deploy", "-d"]:
		deploy()
	else:
		logging.error(DOLPHIN_COMMAND_FUNC_NOTFOUND)

	cleanup()


























