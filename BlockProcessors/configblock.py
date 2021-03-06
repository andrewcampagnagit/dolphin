import json
import yaml
import toml
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

    ##  Prints value from yamlpath
    if block["type"] == "config.print.yaml":
        return print_yaml(block)

    ##	Writes new value to jsonpath
    elif block["type"] == "config.write.yaml":
        return write_yaml(block)

    ##  Prints value from yamlpath
    if block["type"] == "config.print.toml":
        return print_toml(block)

    ##	Writes new value to jsonpath
    elif block["type"] == "config.write.toml":
        return write_toml(block)

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

def print_yaml(block):
	"""Prints value in specified jsonpath for YAML file...
	"""

	json_data = yaml.load(open(block["filepath"], "r").read())
	jsonpath_expression = parse(block["jsonpath"])
	data = jsonpath_expression.find(json_data)

	return "echo \"" + data[0].value +"\"", None, None

def write_yaml(block):
	"""Writes value in specified jsonpath for YAML file...
	"""

	json_data = yaml.load(open(block["filepath"], "r").read())
	jsonpath_expression = parse(block["jsonpath"])
	jsonpath_expression.update(json_data, block["value"])
	data = jsonpath_expression.find(json_data)

	with open(block["filepath"], "w+") as yaml_config_file:
		yaml.dump(json_data, yaml_config_file)
		yaml_config_file.close()

	return "echo \"" + str(json_data) +"\"", None, None

def print_toml(block):
	"""Prints value in specified jsonpath for TOML file...
	"""

	json_data = toml.load(open(block["filepath"], "r"))
	jsonpath_expression = parse(block["tomlpath"])
	data = jsonpath_expression.find(json_data)

	return "echo \"" + data[0].value +"\"", None, None

def write_toml(block):
	"""Writes value in specified jsonpath for TOML file...
	"""

	json_data = toml.load(open(block["filepath"], "r"))
	jsonpath_expression = parse(block["tomlpath"])
	jsonpath_expression.update(json_data, block["value"])
	data = jsonpath_expression.find(json_data)

	with open(block["filepath"], "w") as toml_config_file:
		toml.dump(json_data, toml_config_file)
		toml_config_file.close()

	return "echo \"" + str(json_data) +"\"", None, None