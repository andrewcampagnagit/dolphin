"""
kubectl instruction block processor...
"""


def processblock(block):
    """Required method for all processors
    this is the entry point for parsing commands
    from instruction blocks...
    """

    if block["type"] == "shell":
        return block["cmd"], None, None

    elif block["type"] == "delete":
        return processdelete(block)

    elif block["type"] == "create":
        return processcreate(block)


def processcreate(block):
    """Develops main create command and provides
    var and wait command configuration data...
    """

    main_cmd = var_cmd = wait_for = None

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

    if wait_for["type"] == "PodStatus":
        wait_for["cmd"] = "kubectl describe pod/" + wait_for["selector"] + " -n "+
        wait_for["namespace"] + " |grep Status: |awk '{print $2}'"
        return wait_for
