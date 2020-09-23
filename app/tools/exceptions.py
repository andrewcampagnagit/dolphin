"""
Custom exception messages for error handling.
"""

INSTRUCTION_DL_FUNC_NOTFOUND = """The instructions download function was not found...

Please specify a function <function> <file path/url>

NAME				OPTION				EXPECTS				DESCRIPTION

From file			--file/-f			File path			Downloads from file path
From [GET]			--GET/-G			URL      			Downloads from URL
"""

DOLPHIN_COMMAND_FUNC_NOTFOUND = """The dolphin command function was not found...

Please specify a dolphin function <function> <download function>

NAME				OPTION				EXPECTS				DESCRIPTION

Deploy				deploy/-d			Instructions file	Deploys new application from instructions file
"""