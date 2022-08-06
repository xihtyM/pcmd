# ALL FUNCS AND CLASSES FOR PCMD

# Import

try:
    from all_defs import *
except ImportError as err:
    print("Error importing files.\nERRMSG:", err)
    exit(1)

try:
    from stdcmd import stdcmd_interpret
    STD = True
except ImportError as err:
    errmsg("Error importing standard cmd file, this may cause the program to break.\nERRMSG:", err)
    STD = False
try:
    from cstcmd import cstcmd_interpret
    CUST = True
except ImportError as err:
    CUST = False

# MAIN CMD

def cmd(command: str) -> bool:
    """ Interpret commands with pcmd
        
        Parameters:
            command (str) = The command to run

        Returns:
            True for success and False for error  """
    
    re_implement_std_vars()
    
    # Error checking
    command = command.strip()
    if not command:
        errmsg("Error: Expected at least one argument, got none.")
        return False
    
    command = add_vars(command)

    # Works like cmd args, where every space outside quotes appends to a list of arguments
    ARGS = vargs(command)

    # Error checking
    if not ARGS:
        errmsg("Error: Expected at least one argument, got none.")
        return False
    
    # Length of args
    ARGLEN = len(ARGS)

    # Color text

    rgbl("", color = DEF_COLORS["stdout"], reset_color = False, fin = "")

    if CIS_CMD("captout", arguments = ARGS):
        if ARGLEN < 2:
            errmsg(f"Error: Expected at least 2 arguments, got {ARGLEN}")
            return True
        
        resultIO = StringIO()
        stdout = sys.stdout
        sys.stdout = resultIO
        cmd(
            get_command_from_arg_index(
                command,
                ARGS,
                2
            )
        )
        result = remove_ansi(resultIO.getvalue())
        sys.stdout = stdout
        add_usrvars((ARGS[1], result[0:len(result) - 1]))
        return True
    
    if CIS_CMD("var", arguments = ARGS):
        if ARGLEN < 2:
            errmsg(f"Error: Expected at least 2 arguments, got {ARGLEN}")
            return True
        
        var_name = ARGS[1]

        if ARGLEN == 2:
            add_usrvars((var_name, None))
            return True
        
        variable = get_command_from_arg_index(command, ARGS, 2)
        data_type = get_type(variable)

        try:
            variable = data_type(variable)
        except ValueError:
            errmsg("Error: Could not convert the type")
            add_usrvars((var_name, None))
            return True
        
        add_usrvars((var_name, variable))

        return True
    
    if CIS_CMD("vfree", arguments = ARGS):
        if ARGLEN < 2:
            errmsg(f"Error: Expected at least 2 arguments, got {ARGLEN}")
            return True
        
        variable_list = ARGS[1:]

        for variable in variable_list:
            rem_usrvars(variable)
        
        return True

    if CIS_CMD("if", arguments = ARGS):
        if_b = IF_CMD_INT(ARGS, ARGLEN)
        if type(if_b) == bool:
            print(if_b)
        else:
            cmd(get_command_from_arg_index(command, ARGS, if_b))
        
        return True

    if CIS_CMD("pcmd", OS_FUNC = True, arguments = ARGS):
        path = get_real_path(ARGS[1] if ARGLEN == 2 else command[command.find(ARGS[0]) + len(ARGS[0]):].strip())

        if os.path.isfile(path):
            pcmd_interpret(path)
            return True
        elif os.path.isfile(path + ".pcmd"):
            pcmd_interpret(path + ".pcmd")
            return True
        
        added_path = add_dir(path)

        if os.path.isfile(added_path):
            pcmd_interpret(added_path)
            return True
        elif os.path.isfile(added_path + ".pcmd"):
            pcmd_interpret(added_path + ".pcmd")
            return True
        
        std_comm_pcmd = getcwd() + "/pcmd/" + path

        if os.path.isfile(std_comm_pcmd):
            pcmd_interpret(std_comm_pcmd)
            return True
        elif os.path.isfile(std_comm_pcmd + ".pcmd"):
            pcmd_interpret(std_comm_pcmd + ".pcmd")
            return True

        errmsg("Path is not a file or could not be found:", path)
        return True
    
    if CIS_CMD("echo", "print", arguments = ARGS):
        print(command[command.find(ARGS[0]) + 5:].strip().replace("\\n", "\n").replace("\\t","\t"))
        return True

    if "&&" in ARGS:
        prev = 0
        for _ in range(ARGS.count("&&") + 1):
            new = command.find("&&", prev) if command.find("&&", prev) != -1 else len(command)
            cmd(command[prev:new].strip("&").strip())
            prev = new + 1
        return True

    if CUST:
        CSTCMD_FOUND = cstcmd_interpret(command, ARGS, ARGLEN)
    else:
        CSTCMD_FOUND = False
    
    if CSTCMD_FOUND:
        return True
    
    if STD:
        STDCMD_FOUND = stdcmd_interpret(command, ARGS, ARGLEN)
    else:
        STDCMD_FOUND = False

    if STDCMD_FOUND:
        return True

    errmsg("Command not found:", ARGS[0])
    return False

def pcmd_interpret(file: str) -> None:
    if not os.path.isfile(file):
        return
    
    lines = [i for i in open(file, "r").readlines() if i.strip() != ""]

    for val in lines:
        command = add_vars(val.strip())

        if command[0:2] == "//":
            continue            

        cmd(command)
    return
