# Main file

try:
    from comm import *
except ImportError:
    errmsg("Error importing files, you may want to redownload your current installation, or run the updater.")
    raise SystemExit(1)


def main() -> None:
    """ Main function for pcmd.                                                                                    \n

        This function does not include an interpreter, simply colored text and a simple input for the terminal.
        You may find the standard command interpreter in stdcmd and the custom command interpreter in cstcmd.      \n

        The comm module's cmd function handles interpreting through both cstcmd and stdcmd, it also gives keywords
        like echo, print, vfree, var and captout to name a few - these commands cannot be overwritten and are
        reserved for the comm module only.                                                                         \n

        The all_defs module provides definitions for functions such as rgbl, errmsg, sucmsg, vargs, IS_CMD, all
        user defined variable (USR_DEFINED_VARS) functions and all buffer functions. It contains many more
        functions which you can feel free to take a look at. The functions are written in the fastest way to
        maximize performance and give a programmer an easier time writing with less errors.                       """
    
    rgbl(VARS.directory, color = DEF_COLORS["dir"], fin = "")
    rgbl(" ~ ", color = DEF_COLORS["cmd_seperator"], fin = "", reset_color = False)
    rgbl("", color = DEF_COLORS["cmd"], fin = "", reset_color = False)

    try:
        command = input()
    except KeyboardInterrupt:
        SYS.WaitForKeyboardInterruptOrEOF()
        errmsg("\nError: Command not able to be interpreted")
        return None
    except EOFError:
        SYS.WaitForKeyboardInterruptOrEOF()
        errmsg("Error: Command not able to be interpreted")
        return None
    try:
        cmd(command)
    except KeyboardInterrupt:
        # Press ctrl c to stop commands from running
        SYS.WaitForKeyboardInterruptOrEOF()
        if SYS.win32:
            return None
        else:
            clear_screen()
            return None
    except Exception as err:
        errmsg("Error:", err)
    return None

if __name__ == "__main__":
    while 1:
        main()
    finish()
