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
from instructionparser import InstructionParser

def deploy():
	"""Loads a new parser from mode configuration in instruction block file.
	Each block is then is processed in the parseblock(<block>) method provided
	by the parser. To understand what this method does in depth see the
	comments in the InstructionParser class for the parseblock() method.
	"""

	try:

		# Check if argument was passed and if file exists before proceeding.
		if len(sys.argv) < 3:
			raise Exception("No file path provided")
		if not os.path.exists(sys.argv[2]):
			raise Exception("Couldn't find instruction file " + sys.argv[2])

		with open(sys.argv[2], "r") as instruction_block_file:
			instruction_blocks = json.load(instruction_block_file)

		parser = InstructionParser(instruction_blocks["settings"]["mode"],
								   instruction_blocks["settings"]["varpath"])

		for block in instruction_blocks["blocks"]:
			parser.parseblock(block)

	except Exception as e:
			logging.error(e)

if __name__ == "__main__":

	if sys.argv[1] == "deploy":
		deploy()
	else:
		logging.error("Unknown command "+ sys.argv[1])


























