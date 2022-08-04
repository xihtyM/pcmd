# All defines/functions

class VARS:
    directory = ""

class IMPORTS:
    OS = True
    TIME = True
    SYS = True

class SYS:
    win32 = False
    linux = False

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

def rgbl(* msg: tuple, color: list[int], seperator: str = " ", fin: str = "\n", reset_color: bool = True) -> None:
    """Writes a colored message to the standard output in chosen color"""
    print(rgb(color[0], color[1], color[2], "", end = ""), end = "")
    for index, val in enumerate(msg):
        print(val, end = "")
        if index < len(msg) - 1:
            print(seperator, end = "")
    cleanup = "\u001B[0m" if reset_color else ""
    print(fin, end = cleanup)

def printlines(* msg: tuple, _sep: str = " ", _end: str = "\n") -> None:
    for index, val in enumerate(msg[0]):
        val = str(val) if not type(val) == str else val
        print(val, end = "")
        if index < len(msg):
            print(_sep, end = "")
    print(_end, end = "\u001B[0m")

def errmsg(* msg: tuple, seperator: str = " ", fin: str = "\n") -> None:
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
    
    # List variable of all args to return
    lst = []

    # If in quotation marks variable
    quotes = False

    # If previous char is a space
    previous_space = False

    # Unappended string
    args = ""
    
    # Loop through chars in command
    for chr in command:

        # If char is not a space or inside of quotes
        if chr != " " or quotes:
            
            # If char is a quotation mark
            if chr in ("\"", "\'"):
                quotes = not quotes
                continue

            # If not add char to unappended string and continue
            args += chr
            previous_space = False
            continue
        
        # If the last character is not a space and chr is not in quotes
        if not (previous_space or quotes):
            lst.append(args)
            args = ""
        
        # If chr is a space
        previous_space = True

    # If there are leftover args, append them
    if args:
        lst.append(args)
    
    return lst

try:
    import os
    SYS.linux = os.name == "posix"
    SYS.win32 = os.name == "nt"
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
except ImportError:
    errmsg("Error importing sys module, all sys-related commands have been disabled.")
    IMPORTS.SYS = False

try:
    if SYS.win32:
        import msvcrt
    elif SYS.linux:
        import tty, termios
except ImportError:
    pass

if IMPORTS.OS:
    if SYS.linux:
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
            return ("", open(getcwd() + "/vars/dir", "r", encoding = "utf-8").read()) [os.path.isfile(getcwd() + "/vars/dir")]
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
	for i,val in enumerate(tuple_list):
		if (type(val) == str): tuple_list[i] = val.lower()
	return tuple(tuple_list)

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
    for i in tuple_to_lower(command):
        if i in ("&&", "echo", "print", "pcmd"):
            errmsg(f"Error: Command {i} is reserved for comm.py only, do not use this name")
            return False
    
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
    
    if prefix:
        command_2 = tuple([prefix + "::" + end for end in command])
        return arguments[0].lower() in command or arguments[0].lower() in command_2

    return arguments[0].lower() in command

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
    d_list = os.listdir(path)

    if not d_list:
        return 0
    
    for val in d_list:
        t_path = path + "/" + val
        if os.path.isdir(t_path):
            size += get_directory_size(t_path)
            continue
        size += os.path.getsize(t_path)
    
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
        return msvcrt.getch()
    elif SYS.linux:
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
    return path[0 : find(path, "/", c - 1) - 1 if c > 0 else len(path)]

def pcmd_interpret_env(command: str) -> str:
    return command.replace("{GETVAR(CWD)}", VARS.directory).replace("{GETVAR(DESKTOP)}", get_real_path(os.getenv("USERPROFILE")) + "/Desktop" if SYS.win32 else "/home/desktop").replace("{GETVAR(RUNPATH)}", getcwd())
