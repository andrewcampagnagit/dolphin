import sys
import os
import json
import parse
import heapq
from parse import InstructionParser

with open(sys.argv[1], "r") as instructions_file:
    instruction_blocks = json.load(instructions_file)

if __name__ == "__main__":

    # Generate a new parser to run instruction blocks
    parser = InstructionParser(instruction_blocks["settings"]["mode"],
                               instruction_blocks["settings"]["varpath"])

    # Parses instruction block in top to bottom order from instructions and
    # loads into priority queue
    for block in instruction_blocks["blocks"]:
        parser.parseblock(block)
