# All defines/functions

from ast import literal_eval
from typing import Union as MultipleReturn
import platform as SYSPLAT
import re, subprocess

class VARS:
    directory = ""

class IMPORTS:
    OS = True
    TIME = True
    SYS = True

class SYS:
    win32 = False
    posix = False
    OSNAME = SYSPLAT.system()
    FULLOSNAME = SYSPLAT.platform()
    ARCH = SYSPLAT.machine()
    USRPROFILE = ""
    SYSTEM_VARNAMES = (
        "__CWD__",
        "__RUNPATH__",
        "__USR__",
        "__DESKTOP__",
        "__OSNAME__",
        "__FULLOSNAME__",
        "__ARCH__"
    )
    SYSTEM_VARNAME_PROTECT = False
    PY_VERSION = SYSPLAT.python_version()
    PY_PREFIX = "python3" if PY_VERSION[0] == "3" else "python"
    DEPRECATION_WARNINGS = True

    def WaitForKeyboardInterruptOrEOF() -> None:
        """ Waits to stop KeyboardInterrupt/EOF errors """
        time.sleep(SYS.LOW_FLOAT)

USR_DEFINED_VARIABLES: list[tuple] = [
    # DO NOT ADD DIRECTLY HERE, USE "add_usrvars" FUNCTION
]

# Colors dictionary

COLORS = {
    "red": [255, 0, 0],
    "purple": [159, 60, 230],
    "dark-green": [106, 224, 52],
    "orange": [224, 146, 29],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "cyan": [0, 255, 255],
    "yellow": [255, 255, 0],
    "gray": [100, 100, 100],
    "white": [200, 200, 200],
    "bright-white": [255, 255, 255],
    "light-blue": [51, 150, 191]
}

DEF_COLORS = {
    "dir": COLORS["purple"],
    "cmd_seperator": COLORS["dark-green"],
    "cmd": COLORS["orange"],
    "stdout": COLORS["light-blue"]
}

def rgb(r: int, g: int, b: int, txt: str, end: str = "\u001B[0m") -> str:
    """RGB colored text"""
    r, g, b = str(r), str(g), str(b)
    return f"\u001b[38;2;{r};{g};{b}m{txt}{end}"

def rgbl(* msg, color: list[int], seperator: str = " ", fin: str = "\n", reset_color: bool = True) -> None:
    """Writes a colored message to the standard output in chosen color"""
    print(rgb(color[0], color[1], color[2], "", end = ""), end = "")
    for index, val in enumerate(msg):
        print(val, end = "")
        if index < len(msg) - 1:
            print(seperator, end = "")
    cleanup = "\u001B[0m" if reset_color else ""
    print(fin, end = cleanup)

def printlines(* msg, _sep: str = " ", _end: str = "\n") -> None:
    for index, val in enumerate(msg[0]):
        val = str(val) if not type(val) == str else val
        print(val, end = "")
        if index < len(msg):
            print(_sep, end = "")
    print(_end, end = "\u001B[0m")

def errmsg(* msg, seperator: str = " ", fin: str = "\n") -> None:
    """Writes a message to the standard output in red"""
    print(rgb(200, 0, 0, "", end = ""), end = "")
    printlines(msg, _sep = seperator, _end = fin)

def sucmsg(* msg: tuple, seperator: str = " ", fin: str = "\n") -> None:
    """Writes a message to the standard output in green"""
    print(rgb(0, 200, 0, "", end = ""), end = "")
    printlines(msg, _sep = seperator, _end = fin)

def vargs(command: str) -> list[str]:
    """Turn command string into list of arguments"""

    # Take spaces off of command to save time in for loop
    command = command.strip()

    # If command is only spaces or empty then return nothing
    if not command:
        return []
    
    command = command.replace("\'", "\"")

    in_quotes = False

    # List variable of all args to return
    lst = []

    split_at_quotes = [split_quotes.strip() for split_quotes in command.split("\"") if split_quotes.strip()]
    
    for end in split_at_quotes:
        in_quotes = not in_quotes
        if in_quotes:
            for end_values in end.split():
                lst.append(end_values)
            continue
        lst.append(end)

    return lst

try:
    import os
except ImportError:
    errmsg("Error importing os module, all os-related commands have been disabled.")
    IMPORTS.OS = False
try:
    import time
except ImportError:
    errmsg("Error importing time module, all time-related commands have been disabled.")
    IMPORTS.TIME = False
try:
    import sys
    from io import StringIO
    SYS.posix = sys.platform != "win32"
    SYS.win32 = sys.platform == "win32"
except ImportError:
    errmsg("Error importing sys module, all sys-related commands have been disabled.")
    IMPORTS.SYS = False

try:
    if SYS.win32:
        import msvcrt
    elif SYS.posix:
        import tty, termios
except ImportError:
    pass

if IMPORTS.OS:
    if SYS.posix:
        def clear_screen() -> None:
            os.system("clear")
    elif SYS.win32:
        def clear_screen() -> None:
            os.system("cls")
    if IMPORTS.SYS:
        def getcwd() -> str:
            return os.path.dirname(os.path.realpath(sys.argv[0]))
    else:
        def getcwd() -> str:
            return os.path.dirname(os.path.realpath(os.getcwd()))
    def getdir() -> str:
        try:
            return open(getcwd() + "/vars/dir", "r", encoding = "utf-8").read()
        except FileNotFoundError:
            return "FileNotFoundError"
    def update_dir(path: str) -> bool:
        try:
            open(getcwd() + "/vars/dir", "w", encoding = "utf-8").write(path)
        except FileNotFoundError:
            return False
        VARS.directory = getdir()
        return VARS.directory == path
else:
    def getdir() -> str:
        return ""
    def getcwd() -> str:
            return ""

VARS.directory = getdir()

def tuple_to_lower(tp: tuple) -> tuple:
	"""Returns tuple in all lowercase letters"""
	tuple_list = list(tp)
	for i, val in enumerate(tuple_list):
		if (type(val) == str): tuple_list[i] = val.lower()
	return tuple(tuple_list)

def get_float_place(value: float) -> int:
    place = str(value)[::-1].find(".")
    return place if place != -1 else 0

def CIS_CMD(* command: tuple, OS_FUNC: bool = False, TIME_FUNC: bool = False, arguments: list[str], lwr: bool = True) -> bool:
    if lwr:
        command = tuple_to_lower(command)

    if(len(arguments) < 1):
        return False
    if OS_FUNC and not IMPORTS.OS:
        return False
    if TIME_FUNC and not IMPORTS.TIME:
        return False
    if type(arguments[0]) != str:
        return False
    
    return arguments[0].lower() in command

def IS_CMD(* command: tuple, OS_FUNC: bool = False, TIME_FUNC: bool = False, arguments: list[str], lwr: bool = True, prefix: str = "") -> bool:
    lowered_command = tuple_to_lower(command)
    for i in lowered_command:
        if i in ("&&", "echo", "print", "pcmd", "vfree", "captout", "if", "var"):
            errmsg(f"Error: Command {i} is reserved for comm.py only, do not use this name")
            return False
    
    if lwr:
        command = lowered_command
        prefix = prefix.lower()

    if len(arguments) < 1:
        return False
    
    if OS_FUNC and not IMPORTS.OS:
        return False
    if TIME_FUNC and not IMPORTS.TIME:
        return False
    
    if type(arguments[0]) != str:
        return False
    
    if not prefix:
        return arguments[0].lower() in command
    
    command_2 = tuple([prefix + "::" + end for end in command])
    return arguments[0].lower() in command or arguments[0].lower() in command_2

def remove_path_from(path: str, remove: str) -> str:
    list_of_path_contents = []
    current = ""

    for ch in path:
        if ch != "/" and ch != "\\":
            current += ch
        else:
            list_of_path_contents.append(current)
            current = ""
    
    # If leftover
    if current:
        list_of_path_contents.append(current)
    
    end = ""

    for string in list_of_path_contents:
        if string != remove * len(string):
            end += string + "/"
    
    if SYS.posix:
        end = "/" + end
    
    return end
    
def finish() -> None:
    rgbl(color = [0, 0, 0], fin = "")
    exit(0)

def get_real_path(path: str) -> str:
    no_dots = remove_path_from(path, ".")
    fp = no_dots.strip().replace("\\", "/").rstrip("/")
    formatted_path = ""
    slash = False
    
    for ch in fp:
        if slash and ch == "/":
            continue
        formatted_path += ch
        slash = False
        if ch == "/":
            slash = True

    if(formatted_path == "." * len(formatted_path)):
        return ""
    
    return formatted_path



def get_directory_size(path: str) -> int:
    if not os.path.isdir(path):
        errmsg("Error: Path is not a directory -", path)
        return 0

    size = 0

    d_list = os.scandir(path)

    for entry in d_list:
        try:
            if entry.is_file() and not entry.is_symlink():
                size += entry.stat().st_size
            elif entry.is_dir():
                size += get_directory_size(entry.path)
        except:
            pass
    
    return size


def find(text: str, tofind: str, occurences: int) -> int:
    """Find nth occurence in a string"""
    start = 0
    while occurences >= 0:
        start = text.find(tofind, start + len(tofind))
        occurences -= 1
    return start + 1

def extension(path: str) -> str:
    """Returns the extension of a file/string"""
    return path[find(path, ".", path.count(".") - 1) : len(path)] if path.find(".") != -1 else "N/A"

def getch() -> str:
    """ Waits for a keypress to the stdin file stream                     \n
        Works on linux and windows operating systems                      \n
        Returns: Char inputted whilst waiting """

    if SYS.win32:
        return str(msvcrt.getch(), "utf-8")
    elif SYS.posix:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def convert_denary(num: int, base: int) -> str:
    # Error checking
    base, num = int(base), int(num)
    # Start
    base_num = "";
    while num > 0:
        dig = int(num % base)
        # If base is smaller than 10 then use numbers only
        if dig < 10:
            base_num += str(dig)
        # Else include letters and symbols etc
        else:
            base_num += chr(ord('A') + dig - 10)
        num //= base
    # Invert base_num
    return base_num[::-1]

def convert_to_denary(val: str, base: int) -> int:
    # Error checking
    base, val = int(base), str(val);
    if base < 1 or base > 37:
        raise ValueError("Base must be between 2 and 36");
    # Return decimal value based on the base
    return int(val,base);

def join_args(ARGS: list[str], sep: str = " ") -> str:
    end = ""
    for val in ARGS:
        end += val + sep
    return end

def get_command_from_arg_index(command: str, args: list[str], index: int) -> str:
    end = command

    for i in range(index):
        end = end[len(args[i]):].strip()

    return end

def add_dir(path: str) -> str:
    return VARS.directory + "/" + path

def get_parent(path: str) -> str:
    c = path.count("/")
    if c >= 1:
        if SYS.win32:
            return path[0 : find(path, "/", c - 1) - 1]
        else:
            if c >= 2:
                return path[0 : find(path, "/", c - 2) - 1]
            return path

# MORE VARIABLES

if IMPORTS.OS:
    SYS.USRPROFILE = get_real_path(os.path.expanduser("~/"))

    if not VARS.directory or not os.path.isdir(VARS.directory):
        parent = VARS.directory
        update_dir(SYS.USRPROFILE)
        for i in range(parent.count("/")):
            parent = get_parent(parent)
            if os.path.isdir(parent):
                update_dir(parent)
                break
    
    def get_file_entry_from_directory(file: str) -> os.DirEntry[str]:
        file =  file.lower()
        for entry in os.scandir(VARS.directory + "/"):
            if entry.is_file() and (entry.name.lower().startswith(file + ".") or entry.name.lower() == file):
                return entry
        raise FileNotFoundError("Error: get_file_entry_from_directory() function could not find file:", file)
    
    def get_dir_entry_from_directory(dir: str) -> os.DirEntry[str]:
        dir =  dir.lower()
        for entry in os.scandir(VARS.directory + "/"):
            if entry.is_dir() and entry.name.lower() == dir:
                return entry
        raise FileNotFoundError("Error: get_dir_entry_from_directory() function could not find directory:", dir)

def add_vars(command: str) -> str:

    if command.find("{") == -1 and command.find("}") == -1:
        return command

    c = vargs(command)[0]
    command = command[len(c):].lstrip()

    for USR_VAR in USR_DEFINED_VARIABLES:
        command = command.replace("{" + USR_VAR[0] + "}", str(USR_VAR[1]))
    
    command = c + " " + command

    return command

def add_usrvars(var: tuple[str, any]) -> None:
    if var[0].find("}") != -1 or var[0].find("{") != -1:
        errmsg("Error: Could not create variable, illegal usage - { or } are not allowed for use in variables as they are used to initilize them")
        return
    
    if var[0] in SYS.SYSTEM_VARNAMES and SYS.SYSTEM_VARNAME_PROTECT:
        errmsg(f"Error: Could not create variable, illegal usage - {var[0]} is reserved for system implementation")
        return

    for index, v in enumerate(USR_DEFINED_VARIABLES):
        if v[0] == var[0]:
            USR_DEFINED_VARIABLES[index] = var
            return
    
    USR_DEFINED_VARIABLES.append(var)

def rem_usrvars(var_name: str) -> bool:
    """ Removes a variable from USR_DEFINED_VARIABLES \n
        Returns true if variable was found, otherwise false """
    if var_name in SYS.SYSTEM_VARNAMES and SYS.SYSTEM_VARNAME_PROTECT:
        errmsg(f"Error: Could not remove variable \"{var_name}\" as it is reserved for system implementation")
        return False
    for index, tuples in enumerate(USR_DEFINED_VARIABLES):
        if tuples[0] == var_name:
            USR_DEFINED_VARIABLES.pop(index)
            return True
    errmsg(f"Error: Could not remove variable \"{var_name}\" as it was not found")
    return False
    
def IF_CMD_INT(ARGS: list[str], ARGLEN: int) -> MultipleReturn[int, bool]:
    equal = not_equal = False
    arg1_type = get_type(ARGS[1])
    add = arg1_type(ARGS[1])
    
    if arg1_type == bool:
        add = 1 if ARGS[1] == "True" else 0

    add_2 = ""
    skip = False

    for ind, val in enumerate(ARGS):
        if ind == 0 or skip:
            skip = False
            continue
        
        if val == "+":
            if ind <= 1 or ind >= ARGLEN:
                errmsg(f"If syntax error: Did not expect + at position {ind}")
                return False

            ind_type = get_type(ARGS[ind + 1])
            
            if equal or not_equal:
                if type(add_2) == bool:
                    if add_2 == False:
                        add_2 = 0
                    else:
                        add_2 = 1
                
                if type(add_2) == ind_type:
                    add_2 += ind_type(ARGS[ind + 1])
                elif type(add_2) in (int, float) and ind_type in (int, float):
                    if ind_type == float or type(add_2) == float:
                        add_2 = float(add_2) + float(ARGS[ind + 1])
                    else:
                        add_2 = add_2 + int(ARGS[ind + 1])
                elif type(add_2) != ind_type and ind_type == str:
                    add_2 = str(add_2) + ARGS[ind + 1]
            else:
                if type(add) == bool:
                    if add == False:
                        add = 0
                    else:
                        add = 1
                
                if type(add) == ind_type:
                    add += ind_type(ARGS[ind + 1])
                elif type(add) in (int, float) and ind_type in (int, float):
                    if ind_type == float or type(add_2) == float:
                        add = float(add) + float(ARGS[ind + 1])
                    else:
                        add = add + int(ARGS[ind + 1])
                elif type(add) != ind_type and ind_type == str:
                    add = str(add) + ARGS[ind + 1]
                
            skip = True
        
        if val == "-":
            if ind <= 1 or ind >= ARGLEN:
                errmsg(f"If syntax error: Did not expect - at position {ind}")
                return False
            
            ind_type = get_type(ARGS[ind + 1])
            
            if equal or not_equal:
                if type(add_2) in (int, float) and ind_type in (int, float):
                    if ind_type == float or type(add_2) == float:
                        add_2 = float(add_2) - float(ARGS[ind + 1])
                    else:
                        add_2 = add_2 - int(ARGS[ind + 1])
                else:
                    errmsg(f"If syntax error: Can only subtract numbers at position {ind}")
                    return False
            else:
                if type(add) in (int, float) and ind_type in (int, float):
                    if ind_type == float or type(add) == float:
                        add = float(add) - float(ARGS[ind + 1])
                    else:
                        add = add - int(ARGS[ind + 1])
                else:
                    errmsg(f"If syntax error: Can only subtract numbers at position {ind}")
                    return False

            skip = True

        if val == "==":
            if not_equal or equal or ind >= ARGLEN - 1:
                errmsg(f"If syntax error: Did not expect == at position {ind}")
                return False

            equal = True
            add_2 = get_type(ARGS[ind + 1])(ARGS[ind + 1])
        
        if val == "!=":
            if not_equal or equal or ind >= ARGLEN - 1:
                errmsg(f"If syntax error: Did not expect != at position {ind}")
                return False

            not_equal = True
            add_2 = get_type(ARGS[ind + 1])(ARGS[ind + 1])
        
        if val == "do":
            is_equal = (add == add_2 and equal)
            float_is_equal = ((type(add) == float and type(add_2) == float and (
                add_2 - (5 / 10**get_float_place(add_2))) <= add <= (add_2 + (5 / 10**get_float_place(add_2))
                )
            ) and equal)
            
            is_not_equal = (add != add_2 and not_equal)
            is_str_and_add_or_1 = ((not (not_equal or equal)) and add == 1 or (type(add) == str and not add_2))
            
            end: bool = is_equal or is_not_equal or is_str_and_add_or_1 or float_is_equal
            
            return (ind + 1 if end else end)
        
    is_equal = (add == add_2 and equal)
    float_place_add = get_float_place(add)
    float_precision = 50 ** -float_place_add

    float_is_equal = (type(add) in (int, float) and type(add_2) in (int, float)) and (((add - float_precision) if float_place_add > 4 else add) >= add_2 >= ((add + float_precision) if float_place_add > 4 else add))
    
    is_not_equal = (add != add_2 and not_equal)
    is_str_and_add_or_1 = ((not (not_equal or equal)) and add == 1 or (type(add) == str and not add_2))
    
    end: bool = is_equal or is_not_equal or is_str_and_add_or_1 or float_is_equal
    
    return (end)

def get_type(val: str) -> type:
    try:
        t = literal_eval(val)
        return type(t)
    except:
        return type(val)

def remove_ansi(line: str) -> str:
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def re_implement_std_vars() -> None:
    """ALL STANDARD DEFINED USRVARS - CANNOT BE FREED UNTIL PROGRAM ENDS"""
    
    SYS.SYSTEM_VARNAME_PROTECT = False

    add_usrvars((
        "__CWD__",
        VARS.directory                                                                           # Current directory
    ))

    SYS.SYSTEM_VARNAME_PROTECT = True

def remove_double_slash_comment(line: str) -> str:
    double_slash_comment = False
    in_quotes = False

    double_slash = line.find("//")

    if double_slash == -1:
        return line
    
    start = line.find("\"")
    start = start if start < double_slash and start != -1 else double_slash

    for ind, ch in enumerate(line[start:]):
        if ch == "/" and not in_quotes:
            if double_slash_comment:
                return line[0 : start + ind - 1]
            double_slash_comment = True
            continue
        if ch == "\"":
            in_quotes = not in_quotes
        double_slash_comment = False
    
    return line

def reload_pcmd() -> None:
    if not SYS.DEPRECATION_WARNINGS:
        print("Reloading...")
        MAIN_FILE = getcwd() + "/main.py"
        clear_screen()
        os.startfile(MAIN_FILE)
        finish()
    else:
        errmsg("WARNING: reload_pcmd() function is deprecated as of now")

# ALL VARIABLES

add_usrvars((
    "__USR__",
    SYS.USRPROFILE                                                                           # Path to USRPROFILE
))

add_usrvars((
    "__DESKTOP__",
    SYS.USRPROFILE + "/Desktop"                                                              # Path to desktop
))

add_usrvars((
    "__OSNAME__",
    SYS.OSNAME                                                                               # Operating system short name
))

add_usrvars((
    "__FULLOSNAME__",
    SYS.FULLOSNAME                                                                           # Full operating system name
))

add_usrvars((
    "__ARCH__",
    SYS.ARCH                                                                                 # Architecture computer uses
))

add_usrvars((
    "__RUNPATH__",
    get_real_path(getcwd())                                                                                 # Path to main.py
))

SYS.SYSTEM_VARNAME_PROTECT = True
