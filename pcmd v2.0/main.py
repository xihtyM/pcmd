# Main file

try:
    from comm import *
except ImportError:
    errmsg("Error importing files, you may want to redownload your current installation, or run the updater.")
    exit(1)

while 1:
    rgbl(VARS.directory, color = DEF_COLORS["dir"], fin = "")
    rgbl(" ~ ", color = DEF_COLORS["cmd_seperator"], fin = "", reset_color = False)
    rgbl("", color = DEF_COLORS["cmd"], fin = "", reset_color = False)
    try:
        command = input()
    except KeyboardInterrupt:
        errmsg("\nError: Command not able to be interpreted")
        continue
    except EOFError:
        errmsg("Error: Command not able to be interpreted")
        continue
    try:
        cmd(command)
    except KeyboardInterrupt:
        # Press ctrl c to stop commands from running
        pass
    except Exception as err:
        errmsg("Error:", err)

