#!/usr/bin/env python3
"""
Dolphin - Cloud deployment and packaging framework.
Version: BETA 3.0
Guide: https://github.com/andrewcampagnagit/dolphin/blob/beta-4/docs/GUIDE.md
Version notes:
This version is a beta and does not come with complete functionality and could
contain bugs that negatively impact deployments to production environments.

dolphin project - 2020
"""

from dolphinpkg.instructionparser import InstructionParser
from dolphinpkg.downloader import Downloader
from dolphinpkg.infod.messages import Messages
from dolphinpkg.packager.packager import Packager
from colorama import Fore, Style
import sys, os, json, logging
import time

print(Fore.YELLOW, end="")
print(Messages.get_info_msg("STARTUP"))
print(Style.RESET_ALL, end="")

def deploy():
	"""Each block is then is processed in the parseblock(<block>) method 
	provided by the parser. To understand what this method does in depth see 
	the comments in the InstructionParser class for the parseblock() method.
	"""

	instruction_blocks = None

	print(Fore.WHITE,end="")
	print("Gathering resources...")

	try:
		args = parseargs()

		# Working with manifests - should abstract this...manifests could be files
		if "from_manifest_get" in args.keys():
			print(Fore.YELLOW, end="")
			print("[GET]**************************************************")
			print(Fore.MAGENTA, end="")
			print("Downloading manifest from "+ args["from_manifest_get"])
			print("Placing instructions into /tmp/instructions.json")
			Downloader.download_to(args["from_manifest_get"], 
										"/tmp//manifest.json")
			manifest = json.load(open("/tmp//manifest.json", "r"))

			if "var_url" in manifest.keys():
				args["preload_vars"] = manifest["var_url"]

			if "instructions_url" in manifest.keys():
				args["get_instructions"] = manifest["instructions_url"]

			print(Style.RESET_ALL, end="")

		elif "from_manifest_file" in args.keys():
			print(Fore.YELLOW, end="")
			print("*******************************************************")
			print(Fore.MAGENTA, end="")
			print("Loading manifest from file "+ args["from_manifest_file"])
			manifest = json.load(open(args["from_manifest_file"], "r"))

			if "var_url" in manifest.keys():
				args["preload_vars"] = manifest["var_url"]

			if "instructions_url" in manifest.keys():
				args["get_instructions"] = manifest["instructions_url"]

			print(Style.RESET_ALL, end="")

		# Working with instructions file
		if "get_instructions" in args.keys():
			print(Fore.YELLOW, end="")
			print("[GET]**************************************************")
			print(Fore.MAGENTA, end="")
			print("Downloading instructions from "+ args["get_instructions"])
			print("Placing instructions into /tmp/instructions.json")
			Downloader.download_to(args["get_instructions"], 
										"/tmp/instructions.json")
			instruction_blocks = json.load(open("/tmp/instructions.json", "r"))
			print(Style.RESET_ALL, end="")
		else:
			instruction_blocks = json.load(open(args["instructions_file"], "r"))

		# Working with vars file
		if "preload_vars" in args.keys():
			print(Fore.YELLOW, end="")
			print("[GET]**************************************************")
			print(Fore.MAGENTA, end="")
			print("Downloading vars from "+ args["preload_vars"])
			print("Placing vars into /tmp/vars.json")
			Downloader.download_to(args["preload_vars"], 
								   "/tmp/vars.json")
			instruction_blocks["settings"]["varpath"] = "/tmp/"
			print(Style.RESET_ALL, end="")

		parser = InstructionParser(instruction_blocks["settings"]["varpath"])

		for block in instruction_blocks["blocks"]:
			print(Fore.WHITE,end="")
			print("[INSTRUCTION BLOCK]************************************")
			print(Style.RESET_ALL, end="")
			parser.parseblock(block)

		for test in instruction_blocks["tests"]:
			print(Fore.WHITE,end="")
			print("[TEST BLOCK]*******************************************")
			print(Style.RESET_ALL, end="")
			if not parser.run_test(test):
				print(Fore.RED, end="")
				print("Failed test block")
				print(test["script"])
				raise Exception(Messages.get_exception_msg("5"))
			else:
				print(Fore.GREEN, end="")
				print("PASS")
				print(Style.RESET_ALL, end="")

	except Exception as e:
		print(Fore.RED, end="")
		print(e)
	
	print(Style.RESET_ALL, end="")
	exit()

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
		"-mG":"from_manifest_get",
		"--manifest-get":"from_manifest_get",
		"-mF":"from_manifest_file",
		"--manifest-file":"from_manifest_file"
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

if __name__ == "__main__":

	# Start logging
	logging.basicConfig(level=logging.DEBUG,
	                    format="%(asctime)-15s %(levelname)-8s %(message)s",
	                    stream=sys.stdout)

	print(sys.argv)

	try:
		if len(sys.argv) > 1:
			if sys.argv[1] == "deploy":
				deploy()
			elif sys.argv[1] == "package-create":
				Packager.create_package(sys.argv[2])
			else:
				raise(Exception(Messages.get_exception_msg("3")))
		else:
			print(Messages.get_exception_msg("4"))
	except Exception as e:
		print(e)




