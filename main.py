import vers_ctrl
import sys
import re

h1 = vers_ctrl.HVC()

print(f"{sys.argv}")

# TODO: Make sure arguments in the right order. Statement first followed by arguments for the statments. Shouldn't be allowed to run the other way(Throw error)
# Most likely the first argument after the script name can't start with "-".(First argument after the name needs to be an acceptable statement)
statement = sys.argv[1]
flags = []

for item in sys.argv:
    if re.match("-[a-z]", item):
        flags.append(item)

print(flags)

# Check input is correct before putting into the switch statement
acceptable_statements = [
    "init",
    "add",
    "commit",
    "cat",
    "status",
    "branch",
    "switch",
    "merge",
]

# TODO: Add a switch statement for input
if statement in acceptable_statements:
    match statement:
        case "init":
            pass
        case "add":
            print("add was called")
        case "commit":
            print("commit was called")
        case "cat":
            pass
        case "status":
            pass
        case "branch":
            pass
        case "switch":
            pass
        case "merge":
            pass
else:
    print(f"{statement} is not a hvc statement")


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

# ------------------------------Test Code to be delete ----------------------------
