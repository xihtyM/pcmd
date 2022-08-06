# Custom commands for pcmd

# Import

try:
    from all_defs import *
except ImportError as err:
    print("Error importing files.\nERRMSG:", err)
    exit(1)

def cstcmd_interpret(command: str, ARGS: list[str], ARGLEN: int) -> bool:
    """Custom command interpreter"""
    # Arguments:
    #   command: str - the input taken from the user in the terminal/stdin stream.
    #   ARGS: list[str] - The arguments of that command, basically just vargs(command). A list of strings.
    #   ARGLEN: int - the amount of arguments in the command

    # Proper pcmd syntax:
    # Example:

    # if IS_CMD("command_name", arguments = ARGS):
    #   Do stuff
    #   return True

    # ALWAYS return True if you want to break a function in IS_CMD,
    # Returning False will print out an error saying command not found


    # IS_CMD required parameters:
    #   * command: tuple - put this in first, it will serve as the name of the command.
    #   DO NOT USE SPACES IN THE COMMAND
    #   DO NOT USE THE FOLLOWING STRINGS, IT WILL NOT WORK: "&&", "echo", "print", "pcmd", "captout", "if", "vfree"
    #   For multiple commands use IS_CMD("command_1", "command_2")
    
    #   arguments: list[str] - ALWAYS set this to ARGS unless you know what you are doing.


    # IS_CMD non-required parameters:
    #   OS_FUNC: bool = False - automatically sets this to false
    #   Set this to True if you use the os module anywhere in your commands code

    #   TIME_FUNC: bool = False - automatically sets this to false
    #   Set this to True if you use the time module anywhere in your commands code
    
    #   lwr: bool = True - automatically sets this to true
    #   This makes it so it doesn't matter if the user uses capital letters or lowercase in the command
    #   Set this to False only when you require capitals to be input for your command to work
    
    #   prefix: str = "" - adds a prefix to the command e.g. prefix = "foo" and command = "bar" then it could either be:
    #   foo::bar
    #   or just bar, both work
    #   DO NOT USE STD PREFIX, THIS IS RESERVED FOR STANDARD COMMANDS


    # Code goes here - ALL FUNCTIONS WITH THE SAME NAMES AS STANDARD FUNCTIONS WILL OVERWRITE THE STANDARD DEFINITION

    # Function example:

    """
    if IS_CMD("bar", arguments = ARGS):
        print("foo")
        if ARGLEN == 2:
            print(ARGS[1])
        return True
    """

    # Return false if you wish to print command not found.
    return False
