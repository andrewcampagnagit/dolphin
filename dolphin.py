"""
Dolphin - Cloud deployment and packaging framework.
Version: BETA 3.0
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

from instructionparser import InstructionParser
from downloader import Downloader
from infod.messages import Messages
from colorama import Fore, Style
import sys, os, json, logging
import time

print(Fore.YELLOW, end="")
print(Messages.get_info_msg("STARTUP"))
print(Style.RESET_ALL, end="")

def deploy():
	"""Loads a new parser from mode configuration in instruction block file.
	Each block is then is processed in the parseblock(<block>) method provided
	by the parser. To understand what this method does in depth see the
	comments in the InstructionParser class for the parseblock() method.
	"""

	instruction_blocks = None

	print(Fore.WHITE,end="")
	print("Gathering resources...")

	try:
		args = parseargs()

		if "from_manifest" in args.keys():
			print(Fore.YELLOW, end="")
			print("[GET]**************************************************")
			print(Fore.MAGENTA, end="")
			print("Downloading manifest from "+ args["from_manifest"])
			print("Placing instructions into ./tmp/instructions.json")
			Downloader.download_to(args["get_instructions"], 
										"./tmp/manifest.json")
			manifest = json.load(open("./tmp/manifest.json", "r"))

			if "var_url" in manifest.keys():
				args["preload_vars"] = manifest["var_url"]

			if "instructions_url" in manifest.keys():
				args["get_instructions"] = manifest["instructions_url"]

			print(Style.RESET_ALL, end="")

		if "get_instructions" in args.keys():
			print(Fore.YELLOW, end="")
			print("[GET]**************************************************")
			print(Fore.MAGENTA, end="")
			print("Downloading instructions from "+ args["get_instructions"])
			print("Placing instructions into ./tmp/instructions.json")
			Downloader.download_to(args["get_instructions"], 
										"./tmp/instructions.json")
			instruction_blocks = json.load(open("./tmp/instructions.json", "r"))
			print(Style.RESET_ALL, end="")
		else:
			instruction_blocks = json.load(open(args["instructions_file"], "r"))

		if "preload_vars" in args.keys():
			print(Fore.YELLOW, end="")
			print("[GET]**************************************************")
			print(Fore.MAGENTA, end="")
			print("Downloading vars from "+ args["preload_vars"])
			print("Placing vars into ./tmp/vars.json")
			Downloader.download_to(args["preload_vars"], 
								   "./tmp/vars.json")
			instruction_blocks["settings"]["varpath"] = "./tmp/"
			print(Style.RESET_ALL, end="")

		parser = InstructionParser(instruction_blocks["settings"]["mode"],
								   instruction_blocks["settings"]["varpath"])

		for block in instruction_blocks["blocks"]:
			parser.parseblock(block)

	except Exception as e:
		print(Fore.RED, end="")
		print(e)

	print(Style.RESET_ALL, end="")
	clean_and_exit()

def parseargs():
	"""Helper function to parse command line arguments into a dictionary.
	This makes adding new options and deciphering input easier.
	"""

	parsed = {}

	options = {
		"-f":"instructions_file",
		"--file":"instructions_file",
		"-G":"get_instructions",
		"--GET":"get_instructions",
		"-p":"preload_vars",
		"--preload":"preload_vars",
		"-m":"from_manifest",
		"--manifest"
	}

	current_option = None

	for arg in sys.argv[2:]:
		if arg in options.keys():
			current_option = options[arg]
		else:

			# If there are no options selected for the given argument
			if not current_option:
				raise(Exception(Messages.get_exception_msg("1")))

			parsed[current_option] = arg
			current_option = None

	# Checks that only one method of instruction input is selected
	if all(option in parsed.keys() for option in ["instructions_file",
													"get_instructions"]):
		raise(Exception(Messages.get_exception_msg("2")))

	return parsed

def clean_and_exit():
	"""Cleans up all downloaded files in the ./tmp directory and exits.
	"""

	print("Cleaning up...")
	os.popen("rm .dolphin_last_out.log")
	os.chdir("./tmp")
	os.popen("rm -r *")
	exit()

if __name__ == "__main__":

	try:
		if len(sys.argv) > 1:
			if sys.argv[1] == "deploy":
				deploy()
			else:
				raise(Exception(Messages.get_exception_msg("3")))
		else:
			print(Messages.get_exception_msg("4"))
	except Exception as e:
		print(e)




