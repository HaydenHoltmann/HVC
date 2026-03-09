import vers_ctrl
import sys
import re
import argparse

h1 = vers_ctrl.HVC()
#    "init",
#    "add",
#    "commit",
#    "cat",
#    "status",
#    "branch",
#    "switch",
#    "merge",


# -----------------------------------------------------------argparse (start)---------------------------------------------------------------------------------------
# TODO: argparse functions support additional information, so fill those if necessary after everything works

# Main parser
parser = argparse.ArgumentParser("hvc")


# Subparsers
subparsers = parser.add_subparsers(dest="command")

# init command
init = subparsers.add_parser("init")
# add command
add = subparsers.add_parser("add")

add.add_argument("files", action="store", nargs="+")
# commit command
commit = subparsers.add_parser("commit")
# cat command
cat = subparsers.add_parser("cat")

cat_group = cat.add_argument_group()

# Only allows one of the following arguments to be used
cat_exclusive = cat_group.add_mutually_exclusive_group(required=True)
cat_exclusive.add_argument("-t", action="store_true")
cat_exclusive.add_argument("-p", action="store_true")
cat_exclusive.add_argument("-s", action="store_true")

cat_group.add_argument("hash")

# status command
# branch command
branch = subparsers.add_parser("branch")

branch.add_argument("branch_name", nargs="?")
branch.add_argument("hash", nargs="?")
branch.add_argument("-d", action="store_true", help="Deletes a branch")
# switch command
switch = subparsers.add_parser("switch")

switch.add_argument("branch_name")
# merge command
merge = subparsers.add_parser("merge")

# Getting command line arguments
args = parser.parse_args()

print(args)

match args.command:
    case "init":
        pass
    case "add":
        h1.add(args.files)
    case "commit":
        print("commit was called")
    case "cat":
        if args.t:
            h1.cat(args.hash, "-t")
        elif args.p:
            h1.cat(args.hash, "-p")
        elif args.s:
            h1.cat(args.hash, "-s")
    case "status":
        pass
    case "branch":
        if args.branch_name is None and args.hash is None:
            h1.branch()
        elif args.branch_name is not None:
            if args.d is True:
                h1.branch_delete(args.branch_name)
            else:
                if args.hash is None:
                    h1.branch_new(args.branch_name)
                else:
                    h1.branch_new(args.branch_name, args.hash)
    case "switch":
        pass
    case "merge":
        pass

# -----------------------------------------------------------argparse (start)---------------------------------------------------------------------------------------


# -----------------------------------------------------------Using sys.argv (start)---------------------------------------------------------------------------------------------

# TODO: Make sure arguments in the right order. Statement first followed by arguments for the statments. Shouldn't be allowed to run the other way(Throw error)
# Most likely the first argument after the script name can't start with "-".(First argument after the name needs to be an acceptable statement)
# Add arguments to a list without the first one(which is the name)
# statement = sys.argv[1]
# arguments = []
#
# for i in range(2, len(sys.argv)):
#    arguments.append(sys.argv[i])
#
# flags = []
# modes = []

# Remove the already used arguments(don't need the full list at the moment)
# List flags
# for item in arguments:
#    if re.match("-[a-z]", item):
#        flags.append(item)
#
#
# print(f"Arguments before: {arguments}")
# print(flags)
# List modes
# for item in arguments:
#    print(f"Item: {item}")
#    if re.match("--[a-z]+", item):
#        modes.append(item)
#
## TODO: Add support for additionals, example a message, a hash, etc
# additionals = [x for x in arguments if x not in flags and x not in modes]
#
# print(f"Additionals: {additionals}")
#
#
## Check input is correct before putting into the switch statement
# acceptable_statements = [
#    "init",
#    "add",
#    "commit",
#    "cat",
#    "status",
#    "branch",
#    "switch",
#    "merge",
# ]
#
## TODO: Add a switch statement for input
# if statement in acceptable_statements:
#    match statement:
#        case "init":
#            pass
#        case "add":
#            print("add was called")
#        case "commit":
#            print("commit was called")
#        case "cat":
#            pass
#        case "status":
#            pass
#        case "branch":
#            pass
#        case "switch":
#            pass
#        case "merge":
#            pass
# else:
#    print(f"{statement} is not a hvc statement")


# -----------------------------------------------------------Using sys.argv (end)---------------------------------------------------------------------------------------------

# ------------------------------Test Code to be delete ----------------------------

# h1.hash_object("blob", "what is up, doc?")
# h1.add(".")
# h1.add(["main.py", "vers_ctrl.py", "fake_file.py", "test_file.txt"])
# h1.hash_object("blob", "Some other blob")
# print()
# print(f"Type: {h1.cat('index', '-t')}")
# print(f"Index Content from main: {h1.cat('index', '-p')}")
# print(f"Size: {h1.cat("index", "-s")}")
# print(h1.process_files())
# h1.commit("Master commit for switch test")
# print(h1.cat("6c4e69c4445134fbcc717f0223975a284111d607", "-p"))
# print(h1.test_hashes())
# print(h1.cat("9012aaf549d63e0f1698e28ef60766d7f782c27a", "-t"))
# print(h1.cat("9012aaf549d63e0f1698e28ef60766d7f782c27a", "-p"))
# print(h1.cat("3d2bb751073dd935a59a2d3fa0bf91b783574835", "-t"))
# print(h1.cat("3d2bb751073dd935a59a2d3fa0bf91b783574835", "-p"))
# h1.status()
# h1.branch()
# h1.branch_new("new_branch", "2727574e43302badc6b4501c29e60f6a4ff4d5c0")
# h1.branch_new("new_branch")
# h1.switch("new_branch")
# h1.switch("master")
# print(h1.cat("d2bd604ddc6f6b40ad41e4a9f039b2a002e6e470", "-p"))
# h1.replace_repository("289750daaece6e40d988fc4e31f8dab9eb564abb")
# h1.branch_delete("test_branch")

# ------------------------------Test Code to be delete ----------------------------
