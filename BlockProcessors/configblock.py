"""
config file instruction block processor...
"""

import json
from jsonpath_ng import jsonpath, parse

def processblock(block, varpath):
    """Required method for all processors
    this is the entry point for parsing commands
    from instruction blocks...
    """
    
    ##  Prints value from jsonpath
    if block["type"] == "config.print.json":
        return print_json(block)

    ##	Writes new value to jsonpath
    elif block["type"] == "config.write.json":
        return write_json(block)

def print_json(block):
	"""Prints value in specified jsonpath for JSON file...
	"""

	json_data = json.loads(open(block["filepath"], "r").read())
	jsonpath_expression = parse(block["jsonpath"])
	data = jsonpath_expression.find(json_data)

	return "echo \"" + data[0].value +"\"", None, None

def write_json(block):
	"""Writes value in specified jsonpath for JSON file...
	"""

	json_data = json.loads(open(block["filepath"], "r").read())
	jsonpath_expression = parse(block["jsonpath"])
	jsonpath_expression.update(json_data, block["value"])
	data = jsonpath_expression.find(json_data)

	with open(block["filepath"], "w+") as json_config_file:
		json.dump(json_data, json_config_file)
		json_config_file.close()

	return "echo \"" + str(json_data) +"\"", None, None