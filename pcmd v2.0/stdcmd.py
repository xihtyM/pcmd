# Standard commands for pcmd

# Import

try:
    from all_defs import *
except ImportError as err:
    print("Error importing files.\nERRMSG:", err)
    exit(1)

def stdcmd_interpret(command: str, ARGS: list[str], ARGLEN: int) -> bool:
    """Standard pcmd interpreter for commands"""

    if IS_CMD("if", arguments = ARGS, prefix = "std"):
        equal = not_equal = False
        add = int(ARGS[1]) if ARGS[1].isdigit() else ARGS[1]
        add_2 = ""
        skip = False
        for ind, val in enumerate(ARGS):
            if ind == 0 or skip:
                skip = False
                continue
            
            if val == "+":
                if ind <= 1 or ind >= ARGLEN:
                    errmsg(f"If syntax error: Did not expect + at position {ind}")
                    return True
                
                if equal or not_equal:
                    add_2 = add_2 + int(ARGS[ind + 1]) if type(add_2) == int and ARGS[ind + 1].isdigit() else str(add_2) + ARGS[ind + 1]
                else:
                    add = add + int(ARGS[ind + 1]) if type(add) == int and ARGS[ind + 1].isdigit() else str(add) + ARGS[ind + 1]

                skip = True
            
            if val == "-":
                if ind <= 1 or ind >= ARGLEN:
                    errmsg(f"If syntax error: Did not expect - at position {ind}")
                    return True
                
                if equal or not_equal:
                    if type(add_2) == int and ARGS[ind + 1].isdigit():
                        add_2 = add_2 - int(ARGS[ind + 1])
                    else:
                        errmsg(f"If syntax error: Can only subtract positive integers at position {ind}")
                        return True
                else:
                    if type(add) == int and ARGS[ind + 1].isdigit():
                        add = add - int(ARGS[ind + 1])
                    else:
                        errmsg(f"If syntax error: Can only subtract positive integers at position {ind}")
                        return True

                skip = True

            if val == "==":
                if not_equal or equal or ind >= ARGLEN - 1:
                    errmsg(f"If syntax error: Did not expect == at position {ind}")
                    return True

                equal = True
                add_2 = int(ARGS[ind + 1]) if ARGS[ind + 1].isdigit() else ARGS[ind + 1]
            
            if val == "!=":
                if not_equal or equal or ind >= ARGLEN - 1:
                    errmsg(f"If syntax error: Did not expect != at position {ind}")
                    return True

                not_equal = True
                add_2 = int(ARGS[ind + 1]) if ARGS[ind + 1].isdigit() else ARGS[ind + 1]

            if val == "do":
                if (add == add_2 and equal) or (add != add_2 and not_equal) or ((not (not_equal or equal)) and add == 1 or (type(add) == str and not add_2)):
                    NEW_ARGS = ARGS[ind + 1:]
                    NEW_ARGLEN = len(NEW_ARGS)
                    new_command = get_command_from_arg_index(command, ARGS, ind)

                    if CIS_CMD("echo", "print", arguments = NEW_ARGS):
                        print(new_command[new_command.find(NEW_ARGS[0]) + 5:].strip().replace("\\n", "\n").replace("\\t","\t"))
                        return True

                    SUCCESS = stdcmd_interpret(new_command, NEW_ARGS, NEW_ARGLEN)
                    if not SUCCESS:
                        errmsg("Command not found:", NEW_ARGS[0])
                return True

        print((add == add_2 and equal) or (add != add_2 and not_equal) or ((not (not_equal or equal)) and add == 1 or (type(add) == str and not add_2)))
        
        return True

    if IS_CMD("cls", "clear", OS_FUNC = True, arguments = ARGS, prefix = "std"):
        clear_screen()
        return True
    
    if IS_CMD("cd", OS_FUNC = True, arguments = ARGS, prefix = "std"):
        # Guard
        if ARGLEN < 2:
            errmsg("Error: Expected at least 2 args, got", ARGLEN)
            return True
        
        path = get_real_path(ARGS[1] if ARGLEN == 2 else command[command.find(ARGS[1]):])

        if path[0 : path.find("/") if path.count("/") != 0 else len(path)] in os.listdir(VARS.directory + "/") and path:
            path = VARS.directory + "/" + path
        
        if path[1] != ":" and SYS.win32:
            errmsg("Error: Path does not exist")
            return True

        if os.path.isdir(path):
            if not update_dir(path):
                errmsg("Error: Could not update path variable")
        elif os.path.isfile(path):
            errmsg("Error: Path entered is a file")
        else:
            errmsg("Error: Path does not exist -", path)

        return True
    
    if IS_CMD("dir", OS_FUNC = True, arguments = ARGS, prefix = "std"):
        if ARGLEN == 1:
            path = VARS.directory
        elif ARGLEN == 2:
            path = ARGS[1] if os.path.isdir(ARGS[1]) else VARS.directory + "/" + ARGS[1]
        else:
            path = command[command.find(ARGS[1]):] if os.path.isdir(get_real_path(command[command.find(ARGS[1]):])) else VARS.directory + command[command.find(ARGS[1]):]
        
        path = get_real_path(path)

        if not os.path.isdir(path):
            errmsg("Error: Path does not exist.")
            return True
        
        print(f"\nDirectory of {path}\n")

        full_size = files = folders = 0
        
        path += "/"
        
        for p in os.listdir(path):
            t_path = path + p
            if os.path.isdir(t_path):
                size = get_directory_size(t_path)
                spaces = " " * (20 - len(str(size)))
                print(f"{size} byte(s){spaces}<Dir> {p}")
                full_size += size
                folders += 1
                continue
            size = os.path.getsize(t_path)
            spaces = " " * (20 - len(str(size)))
            print(f"{size} byte(s){spaces}<File> {p}")
            full_size += size
            files += 1
        
        print(f"\n\t{full_size} byte(s)\n\t{files} file(s)\n\t{folders} dir(s)\n")

        return True
    
    if IS_CMD("rd", arguments = ARGS, prefix = "std"):
        directory = VARS.directory
        if directory.count("/") - 1 >= 0:
            update_dir(directory[0 : find(directory, "/", directory.count("/") - 1) - 1])
        else:
            errmsg("Error: Cannot have a null path")
        return True
    
    if IS_CMD("exit", "quit", "close", arguments = ARGS, prefix = "std"):
        finish()
    
    if IS_CMD("color", "colour", arguments = ARGS, prefix = "std"):
        # Guard
        if ARGLEN < 2:
            errmsg(f"Error: Expected at least 2 args, got {ARGLEN}.")
            return True

        operator = ARGS[1]

        if operator in ("-r", "-reset", "reset"):
            DEF_COLORS["cmd"] = COLORS["orange"]
            DEF_COLORS["cmd_seperator"] = COLORS["dark-green"]
            DEF_COLORS["dir"] = COLORS["purple"]
            DEF_COLORS["stdout"] = COLORS["light-blue"]
            return True

        # Guard
        if ARGLEN != 3:
            errmsg(f"Error: Expected 3 args, got {ARGLEN}.")
            return True
        
        color = ARGS[2]

        if not color in COLORS:
            errmsg(f"Color does not exist: {ARGS[2]}\nSee -colors for more info.")
            return True
        
        operator = operator.replace("-c", "cmd").replace("-s", "cmd_seperator").replace("-d", "dir").replace("-t", "stdout")

        if operator in DEF_COLORS:
            DEF_COLORS[operator] = COLORS[color]
            return True
        
        if operator in ("-a", "-all"):
            DEF_COLORS["dir"] = COLORS[color]
            DEF_COLORS["cmd_seperator"] = COLORS[color]
            DEF_COLORS["cmd"] = COLORS[color]
            DEF_COLORS["stdout"] = COLORS[color]
            return True
        
        errmsg("Syntax error: See -colors for more info.")
        return True
    
    if IS_CMD("wait", TIME_FUNC = True, arguments = ARGS, prefix = "std"):
        if ARGLEN < 2:
            time.sleep(1)
            return True
        
        if ARGLEN > 2:
            errmsg(f"Error: Expected at most 2 arguments, got {ARGLEN}")
            return True
        
        try:
            time.sleep(float(ARGS[1]))
        except ValueError:
            errmsg("Error: Number must be a valid, python floating point value")
        return True

    if IS_CMD("pause", arguments = ARGS, prefix = "std"):
        print("Press any key to continue . . .")
        getch()
        return True
    
    if IS_CMD("base", arguments = ARGS, prefix = "std"):
        if ARGLEN < 3:
            errmsg("Syntax error: type '-base' for info.")
            return True
        if ARGLEN == 4:
            # Set what base you are converting from, and to in these variables.
            _from = ARGS[1]
            to = ARGS[2]
            value = ARGS[3]
        else:
            # If there is only 1 "-", then presume that the value after "#" is in denary and set variables accordingly.
            to = ARGS[1]
            _from = 10
            value = ARGS[2]
        try:
            # Convert to and _from variables to integers
            to, _from = int(to), int(_from)
        # Error catching.
        except ValueError as err:
            errmsg("Error converting values: This may be due to a syntax error, type '-base' for info.\nERRMSG:", err)
            return True
        # Convert to the stated base digit.
        try:
            if _from != 10:
                value = convert_to_denary(value, _from)
            print(convert_denary(int(value), to))
        # Error catching.
        except Exception as err:
            errmsg("Error:", err, "\nThis may be due to a syntax error, type '-base' for info.")

        return True
    
    if IS_CMD("-base", arguments = ARGS, prefix = "std"):
        rgbl("\nSyntax:\nbase from *to value\n\nExample:\nbase 2 10 1010\nOutput:\n10\n\nIf you do not include what base you are converting from, pycmd will assume it to be base10.\n", color = [115, 105, 115])
        return True
    
    if IS_CMD("mkdir", OS_FUNC = True, arguments = ARGS, prefix = "std"):
        if ARGLEN != 2:
            errmsg(f"Error: Expected 2 arguments, got {ARGLEN}")
            return True
        directory_name = ARGS[1]
        full_dir = add_dir(directory_name)
        
        end_dir = directory_name if os.path.isdir(get_parent(directory_name)) else full_dir
        parent = get_parent(end_dir)

        if os.path.isdir(end_dir):
            errmsg("Error: Path already exists")
            return True
        
        if end_dir == directory_name and not os.path.isdir(parent):
            errmsg("Error: Parent directory does not exist", parent)
            return True

        os.mkdir(end_dir)

        sucmsg("Sucessfully created directory:", end_dir) if os.path.isdir(end_dir) else errmsg("Failed to create directory:", end_dir)

        return True
    
    

    return False
