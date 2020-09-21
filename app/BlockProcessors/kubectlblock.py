"""
kubectl instruction block processor...
"""


def processblock(block):
    """Required method for all processors
    this is the entry point for parsing commands
    from instruction blocks...
    """
    
    ##  Basic shell commands can be executed using this block type. This is
    ##  good for displaying status deployment information, metadata, and
    ##  testing templates.
    if block["type"] == "shell":
        return block["cmd"], None, None

    ##  Deletes resource specified in the block
    elif block["type"] == "delete":
        return processdelete(block)

    ## Creates resource specified in the block
    elif block["type"] == "create":
        return processcreate(block)


def processcreate(block):
    """Develops main create command and provides
    var and wait command configuration data...
    """

    main_cmd = var_cmd = wait_for = None

    ##  Creates a resource from a Kubernetes YAML file
    if block["from"]["type"] == "file":
        main_cmd = "kubectl create -f resources/" + block["from"]["path"]

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

    if block["from"]["type"] == "file":
        main_cmd = "kubectl delete -f resources/" + block["from"]["path"]

    if "vars" in block.keys():
        var_cmd = []
        for varname in block["vars"].keys():
            var_cmd.append(processvarcmd(varname, block["vars"][varname]))

    if "wait_for" in block.keys():
        wait_for = []
        for wait_block in block["wait_for"]:
            wait_for.append(processwaitfor(wait_block))

    return main_cmd, var_cmd, wait_for


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
