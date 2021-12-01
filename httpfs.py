#! /usr/bin/python3
import sys
from env import Debug, Q_HTTP
from httpfs_lib import httpserver, run_server

verbose = False
directory = None

port = 8080
host = ""  # localhost


def main(argv):
    """The Entry Point of httpfs"""
    global verbose, directory, port

    if len(argv) == 1 and argv[0] == "help":
        help_info = """\nhttpfs is a simple file server.

    Usage:
        httpfs [-v] [-p PORT] [-d PATH-TO-DIR]

    The commands are:
        -v      Prints debugging messages.
        -p      Specifies the port number that the server will listen and serve at. (Default is 8080)
        -d      Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application."""

        print(help_info)

    elif len(argv) == 1 and argv[0] == "info":
        info = "Develped by:\n@starfreck (https://github.com/starfreck)\n@ninanee (https://github.com/ninanee)"
        print(info)

    else:
        # Process verbose
        if "-v" in argv:
            argv.remove("-v")
            verbose = True
        # Process port
        if "-p" in argv:
            location = argv.index("-p")
            argv.remove("-p")
            port = argv[location]
            argv.remove(port)
        # Process Directory
        if "-d" in argv:
            location = argv.index("-d")
            argv.remove("-d")
            directory = argv[location]
            argv.remove(directory)

        if Debug:
            print("\nverbose:", verbose, "Port:", port, "Directory:", directory, "\n")
        # Run Server
        run_server(port=port, verbose=verbose, directory=directory)


def filter_args(argv):
    """handle users wrong cmd input"""
    for arg in argv:
        if len(arg) == 3 and "--" in arg:
            index = argv.index(arg)
            argv[index] = arg.replace("--", "-")
    return argv


if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    argv = filter_args(sys.argv)
    main(argv)
