"""
kubectl instruction block processor...
"""

import requests

def processblock(block, varpath):
    """Required method for all processors
    this is the entry point for parsing commands
    from instruction blocks...
    """
    
    ##  Basic shell commands can be executed using this block type. This is
    ##  good for displaying status deployment information, metadata, and
    ##  testing templates.
    if block["type"] == "kubectl.shell":
        return shell(block)

    ##  Deletes resource specified in the block
    elif block["type"] == "kubectl.delete":
        return processdelete(block)

    ## Creates resource specified in the block
    elif block["type"] == "kubectl.create":
        return processcreate(block, varpath)

def _insertvars(block, varpath):
    """Inserts vars into Kubernetes resource file...
    """

    with open(varpath + "vars.json", "r") as var_file:
            var_dict = json.load(var_file)

    resource = open(block["from"]["path"], "r").read()

    while "%" in resource:
        index_1 = resource.find("%") + 1
        index_2 = resource.find("%", index_1 + 1)
        variable = resource[index_1:index_2]
        resource_file = resource.replace(
            "%" + variable + "%", var_dict[variable])

    with open(block["from"]["path"], "w+") as resource_file:
        resource_file.write(resource)
        resource_file.close()

def processcreate(block, varpath):
    """Develops main create command and provides
    var and wait command configuration data...
    """

    main_cmd = var_cmd = wait_for = None

    ##  Creates a resource from a Kubernetes YAML file
    if block["from"]["type"] == "file":
        main_cmd = "kubectl create -f resources/" + block["from"]["path"]
        _insertvars(block["from"]["file"], varpath)

    ##  Creates a resource from a remote Kubernetes YAML file with [GET]
    elif block["from"]["type"] == "GET":
        resource_data = requests.get(block["from"]["url"]).content

        with open("tmp.yaml", "w+") as resource_file:
            resource_file.write(resource_data.decode("utf8"))

        main_cmd = "kubectl create -f tmp.yaml"
        _insertvars("tmp.yaml", varpath)

    if "vars" in block.keys():
        var_cmd = []
        for varname in block["vars"].keys():
            var_cmd.append(processvarcmd(varname, block["vars"][varname]))

    if "wait_for" in block.keys():
        wait_for = []
        for wait_block in block["wait_for"]:
            wait_for.append(processwaitfor(wait_block))

    return main_cmd, var_cmd, wait_for


def processdelete(block):
    """Develops main delete command and provides
    var and wait command configuration data...
    """

    main_cmd = var_cmd = wait_for = None

    ##  Deletes a resource from a Kubernetes YAML file
    if block["from"]["type"] == "file":
        main_cmd = "kubectl delete -f resources/" + block["from"]["path"]

    ##  Deletes a resource from a remote Kubernetes YAML file with [GET]
    elif block["from"]["type"] == "GET":
        resource_data = requests.get(block["from"]["url"]).content

        with open("tmp.yaml", "w+") as resource_file:
            resource_file.write(resource_data.decode("utf8"))

        main_cmd = "kubectl delete -f tmp.yaml"

    if "vars" in block.keys():
        var_cmd = []
        for varname in block["vars"].keys():
            var_cmd.append(processvarcmd(varname, block["vars"][varname]))

    if "wait_for" in block.keys():
        wait_for = []
        for wait_block in block["wait_for"]:
            wait_for.append(processwaitfor(wait_block))

    return main_cmd, var_cmd, wait_for

def shell(block):
    """Develops main shell command and provides
    var and wait command configuration data...
    """

    main_cmd = var_cmd = wait_for = None

    if "vars" in block.keys():
        var_cmd = []
        for varname in block["vars"].keys():
            var_cmd.append(processvarcmd(varname, block["vars"][varname]))

    if "wait_for" in block.keys():
        wait_for = []
        for wait_block in block["wait_for"]:
            wait_for.append(processwaitfor(wait_block))

    return block["cmd"], var_cmd, wait_for

def processvarcmd(varname, varblock):
    """Generates var command dictionary...
    """

    ##  Store ClusterIP of specified Kubernetes service type resource
    if varblock["type"] == "ClusterIP":
        return (
            varname,
            "kubectl describe svc/" +
            varblock["service"] +
            " -n " +
            varblock["namespace"] +
            " |grep IP: |awk '{print $2}'")

    ## Store contents of last stdout to a variable
    elif varblock["type"] == "STDOUT":
        with open(".dolphin_last_out.log", "r") as dolphin_log_file:
            dolphin_stdout_last = dolphin_log_file.read()

        return (
            varname,
            "cat .dolphin_last_out.log"
            )

    ## Prompt for user input 
    elif varblock["type"] == "prompt":
        value = input(varblock["msg"] + ": ")
        return (varname, "echo \"" + value + "\"")

    else:
        return None


def processwaitfor(wait_for):
    """Generates wait_for command dictionary...
    """

    ##  Waits for specified Kubernetes pod type resource to have a STATUS
    ##  that matches the value (blocks[n].wait_for.value)
    if wait_for["type"] == "PodStatus":
        wait_for["cmd"] = (
                        "kubectl describe pod/"+
                        wait_for["selector"] +
                        " -n "+ wait_for["namespace"] +
                        " |grep Status: |awk '{print $2}'")
        return wait_for
