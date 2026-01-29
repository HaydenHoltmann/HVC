import shutil
import os
import hashlib
import zlib
from pathlib import Path
import re
import datetime
import time


class HVC:
    # Initializes a directory as a repository
    def __init__(self):
        self.template_directory = "Template/"
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.ignore_content = self.process_ignore()
        self.repository_directory = self.cwd + "/.hvc"
        self.objects_directory = self.repository_directory + "/objects"
        self.directory_files = self.process_files()
        self.object_types = {"blob": "000001", "tree": "000002", "commit": "000003"}
        self.variables = self.get_variables()
        self.head = self.get_head()

    def init(self):
        # TODO: Change template directory to config install/wherever install files go directory
        # Install script/Installation method must create the Template folder
        # file_path = os.path.abspath(__file__)

        if not os.path.exists(self.repository_directory):
            shutil.copytree(self.template_directory, self.repository_directory)
            print(f"Initialized new HVC repository in {self.repository_directory}")
        else:
            print("Directory already exists.")

    def hash_object(self, obj_type, content, flag="-c"):
        header = f"{obj_type} {len(content.encode('utf-8'))}\0"

        to_hash = header + content

        # Hashing Stuff
        obj_hash = hashlib.sha1(to_hash.encode("utf-8"))

        sha1 = obj_hash.hexdigest()

        if flag == "-n":
            return sha1

        # Compression Stuff
        zlib_content = zlib.compress(to_hash.encode("utf-8"))

        # File Stuff
        if obj_type == "index":
            path = Path(".hvc/index")
        else:
            # path = Path(".hvc/objects/" + sha1[0:2] + "/" + sha1[2:])
            path = Path(f"{self.objects_directory}/" + sha1[0:2] + "/" + sha1[2:])

        path.parent.mkdir(exist_ok=True, parents=True)

        path.write_bytes(zlib_content)

    # Add creates an index and also adds the objects to the objects folder
    def add(self, files):
        if files[0] == ".":
            index_hashes = []
            dir_files = []

            # Hashes and creates an object for every file in the repository
            for i in self.directory_files:
                if not os.path.isdir(i):
                    object = open(i)
                    object_data = object.read()
                    self.hash_object("blob", object_data)
                    index_hashes.append(self.hash_object("blob", object_data, "-n"))
                    dir_files.append(i)

            # Constructing index content for hashing
            index_content = []
            if len(dir_files) == len(index_hashes):
                for j in range(len(dir_files)):
                    interim_data = f"{index_hashes[j]} {dir_files[j]}"
                    index_content.append(interim_data)

            # Adds all files in the repository to the index
            self.update_index("\n".join(index_content))
        else:
            # Files that are actually part of the directory
            valid_files = []
            # The hash values of the valid files
            valid_index_hashes = []

            # Checks for valid file names
            for i in range(len(files)):
                if files[i] in self.directory_files:
                    valid_files.append(files[i])
                else:
                    print(f"{files[i]} not a part of this repository")

            # Creating the objects, not updating index file
            for i in valid_files:
                if not os.path.isdir(i):
                    object_valid = open(i)
                    object_valid_data = object_valid.read()
                    self.hash_object("blob", object_valid_data)
                    valid_index_hashes.append(
                        self.hash_object("blob", object_valid_data, "-n")
                    )

            # Return values of current index
            current_index = str(self.cat("index", "-p"))
            index_dictionary = {}

            # Split each entry into it's hash and file name values and add it to the dictionary
            current_index_list = current_index.split("\n")

            # Index content to be hashed
            valid_index_content = []

            for ci in current_index_list:
                index_list = ci.split(" ")
                current_hash = index_list[0]
                current_file = index_list[1]

                # Dictionary
                index_dictionary[current_file] = current_hash

            for i in range(len(valid_files)):
                if valid_files[i] in index_dictionary:
                    index_dictionary[valid_files[i]] = valid_index_hashes[i]

            # Add new values from dictionary valid_index_content
            for name in index_dictionary:
                valid_index_content.append(f"{index_dictionary[name]} {name}")

            # Hashing valid files
            self.update_index("\n".join(valid_index_content))

    def update_index(self, content):
        self.hash_object("index", content)

    def process_ignore(self):
        # Git tracks gitignore
        ignore_file = open(".hvc_ignore")
        ignore_output = []

        # TODO: Add support for things like file types etc. that need to be in an ignore file. You might have to separate into different lists
        for line in ignore_file:
            if line[0] == "#" or line == " " or line == "\n":
                pass
            elif line[0] == "/":
                ignore_output.append(line[1 : len(line) - 1])
            else:
                ignore_output.append(line[: len(line) - 1])

        ignore_output.append(".hvc")

        ignore_file.close()

        return ignore_output

    # Returns the content of a compressed object file(including index)
    def cat(self, hash, flag):
        # File on object type
        if hash == "index":
            hashed_file = open(f"{self.repository_directory}/index", "rb")

        else:
            hash_folder = hash[:2]
            hash_file = hash[2:]

            hashed_file = open(
                f"{self.objects_directory}/{hash_folder}/{hash_file}", "rb"
            )

        # Decompression
        toUnhash = hashed_file.read()
        unhashed_content = zlib.decompress(toUnhash)

        # Processing
        content_split = unhashed_content.split(b"\0")
        object_content = content_split[1].decode("utf-8")
        object_type = content_split[0].split(b" ")[0].decode("utf-8")
        object_size = content_split[0].split(b" ")[1].decode("utf-8")

        # Output on flag
        if flag == "-p":
            return object_content
        elif flag == "-t":
            return object_type
        elif flag == "-s":
            return object_size

    # Returns all the names of all the files in the directory and subdirectories, excluding those in the ignore file
    def process_files(self):
        files = []

        the_path = Path(".")
        file_paths = []

        # Add files to file_paths
        for i in the_path.rglob("*"):
            file_paths.append(str(i))

        ignore_paths = []

        # Creates a list of paths that are in the ignore list
        for j in range(len(self.ignore_content)):
            for k in range(len(file_paths)):
                if self.ignore_content[j] in file_paths[k]:
                    ignore_paths.append(file_paths[k])

        # Removes the ignore paths from the list of all the file paths and puts it in it's final list
        files = [x for x in file_paths if x not in ignore_paths]

        return files

    # Creates commit objects. Every time a commit object is created, it will be different because the parent object in the file will be different and also the time
    def commit(self, message):
        # TODO: Can't commit if untracked changes
        # TODO: Make sure you add commits to whatever branch HEAD is pointing to

        # Creates tree object for each directory -------
        directories = []
        rm_trees = []
        commit_tree = ""

        # Adds to a list only directories in the repository(used reverse to add folders in reverse order, don't need to do it again)
        for file in reversed(self.directory_files):
            if os.path.isdir(file):
                directories.append(file)

        # Add root directory to list
        directories.append(self.cwd)

        # Track files. If folder empty, it does not become a tree object
        for paths in directories:
            tree_path = ""
            # Directory has files
            if os.listdir(paths):
                # Creates a tree file in the parent directory
                # TODO:Change tree objects from a .txt file to a extensionless file (The tree files are the only ones with the .txt
                # because python gets confused with the folder of the same name in the current directory)
                if not os.path.dirname(paths):
                    tree_path = f"{os.path.basename(paths)}.txt"
                    tree = open(tree_path, "w")
                else:
                    tree_path = (
                        f"{os.path.dirname(paths)}/{os.path.basename(paths)}.txt"
                    )
                    tree = open(tree_path, "w")

                rm_trees.append(tree_path)
                # Get a list of the files in the current path
                tree_files = []
                for x in os.listdir(paths):
                    if (
                        not os.path.isdir(f"{paths}/{x}")
                        and x not in self.ignore_content
                    ):
                        tree_files.append(x)

                # Hash files in path and append them to tree file
                for file in tree_files:
                    # TODO: When tree objects change to extensionless, this will change as well
                    if paths == self.cwd:
                        tree_directory = file.replace(".txt", "")
                    else:
                        tree_directory = f"{paths}/{file.replace('.txt', '')}"

                    if tree_directory in directories:
                        obj_type = "tree"
                    else:
                        obj_type = "blob"

                    # Not creating the objects, just returning the hashes
                    object_hash = self.hash_object(
                        obj_type, open(f"{paths}/{file}").read(), "-n"
                    )
                    object_entry = [
                        self.object_types[obj_type],
                        obj_type,
                        object_hash,
                        file,
                    ]

                    tree.write(" ".join(object_entry) + "\n")

                tree.close()

                # Hash tree file(This is where the tree objects are created)
                tree = open(tree_path, "r")
                content = tree.read()
                self.hash_object("tree", content)
                # Add root directory hash to commit_tree
                if paths == self.cwd:
                    commit_tree = self.hash_object("tree", content, "-n")
                tree.close()

        for trees in rm_trees:
            if os.path.exists(trees):
                os.remove(trees)

        # Creates commit object -------

        # Content.txt contains the current tree and the parent commit, while the log contains the parent commit and the current commit
        commit_file = open("commit", "w")
        commit_content = []

        commit_content.append(f"tree {commit_tree}")

        # Commit Variables:
        # commit_tree - tree hash
        # parent_hash
        # author
        # message

        # If no master file exists, then it is the first commit so don't add a parent. If a new branch is created, it's parent will be the commit
        # it branches from, so it has a parent

        parent_hash = "0000000000000000000000000000000000000000"

        if not os.path.exists(f"{self.repository_directory}/{self.head}"):
            print("master doesn't exist")
        else:
            head_branch = open(f"{self.repository_directory}/{self.head}")
            parent_hash = head_branch.read()
            commit_content.append(f"parent {parent_hash}")
            head_branch.close()

        commit_time = datetime.datetime.now()
        commit_stamp = int(commit_time.timestamp())
        commit_author = f"{self.variables['author']} {commit_stamp}"
        commit_commiter = f"{self.variables['commiter']} {commit_stamp}"

        # TODO: Add UTC offset to the timestamp
        commit_content.append(commit_author)
        commit_content.append(commit_commiter)

        commit_content.append(f"\n{message}")

        commit_file.write("\n".join(commit_content))

        commit_file.close()

        commit_file = open("commit", "r")
        commit_file_content = commit_file.read()

        self.hash_object("commit", commit_file_content)
        commit_hash = self.hash_object("commit", commit_file_content, "-n")

        commit_file.close()

        # TODO: Delete commit.txt\
        if os.path.exists("commit"):
            os.remove("commit")

        # Creates "master" branch file in refs -------
        new_head_branch = open(f"{self.repository_directory}/{self.head}", "w")

        new_head_branch.write(str(commit_hash))

        new_head_branch.close()

        # Creates logs for tracking changes -------

        # If folders doesn't exist create it
        if not os.path.exists(f"{self.repository_directory}/logs/refs/heads"):
            os.makedirs(f"{self.repository_directory}/logs/refs/heads")
            # add "tag" logs when creating tag

        # If file doesn't exist create it
        log_head = open(f"{self.repository_directory}/logs/{self.head}", "a")
        log_data = []

        current_head = open(f"{self.repository_directory}/{self.head}", "r")
        current_head_content = current_head.read()

        log_data.extend(
            [parent_hash, current_head_content, commit_author, f"commit: {message}"]
        )

        current_head.close()

        log_head.write(f"{' '.join(log_data)}\n")

        log_head.close()

        # Create HEADS in logs -------

        # HEADS tracks all commits made in every branch in the order they are made as well as when branches are switched
        head = open(f"{self.repository_directory}/logs/HEAD", "a")

        head.write(f"{' '.join(log_data)}\n")

        head.close()

        # Create and store last commit message in a COMMIT_EDITMSG file -------
        last_commit_msg = open(f"{self.repository_directory}/COMMIT_EDITMSG", "w")
        last_commit_msg.write(message)
        last_commit_msg.close()

        # TODO: Message confirming commit operation is complete(Add something from status to show changes between files)
        commit_confirmation_message = []

        if parent_hash == "0000000000000000000000000000000000000000":
            root_msg = "(root-commit)"
        else:
            root_msg = ""

            # open status_and_commits.png
        commit_confirmation_message.extend(
            [
                f"[{os.path.basename(self.head)}",
                root_msg,
                f"{current_head_content}] ",
                message,
            ]
        )
        print(commit_confirmation_message)

    # Tracks changes to files
    def status(self):
        branch_file = open(f"{self.repository_directory}/{self.head}", "r")
        last_commit_hash = branch_file.read()

        # print(last_commit_hash)

    # Lists branches
    def branch(self):
        branches = os.listdir(f"{self.repository_directory}/refs/heads")
        current_head = os.path.basename(self.head)

        for br in branches:
            if br == current_head:
                br = br + " *"

            # Lists branches in console
            print(br)

    # Creates a new branch
    def branch_new(self, name, commit=""):
        branch_path = f"{self.repository_directory}/refs/heads/{name}"

        # Only a commit will be able to change the commit object this branch points to
        if os.path.exists(branch_path):
            print(f'A branch called "{name}" already exists.')
        else:
            new_branch = open(branch_path, "w")

            if commit == "":
                current_branch = open(f"{self.repository_directory}/{self.head}", "r")
                current_commit = current_branch.read()

                new_branch.write(current_commit)
                current_branch.close()
            else:
                hash_list = []
                hash_folders = os.listdir(self.objects_directory)

                # Find full hashes using the object folders
                for hf in hash_folders:
                    hash_list.append(
                        f"{hf}{os.listdir(f'{self.objects_directory}/{hf}')[0]}"
                    )

                # Compare against objects
                if commit in hash_list and self.cat(commit, "-t") == "commit":
                    new_branch.write(commit)
                else:
                    print(f"{commit} is not a commit object in this repository")

            new_branch.close()

    # Switches between branches
    def switch(self, name):
        # Don't switch if already on branch "name"
        if name == os.path.basename(self.head):
            print(f'Already on "{name}" branch')
            return

        # TODO: Can't switch if there is uncommited files

        # Make sure that name is an actual branch
        branch_path = f"{self.repository_directory}/{os.path.dirname(self.head)}"
        branches = os.listdir(branch_path)

        if name in branches:
            # Point HEAD to new branch
            head = open(f"{self.repository_directory}/HEAD", "r")
            head_content = head.read()
            head.close()

            # Getting the hash of the commit of the old branch
            old_branch = open(f"{self.repository_directory}/{self.head}", "r")
            old_branch_hash = old_branch.read()
            old_branch.close()
            old_branch_name = os.path.basename(self.head)

            # Writes new branch to point to
            new_head = open(f"{self.repository_directory}/HEAD", "w")
            new_head.write(f"{os.path.dirname(head_content)}/{name}")
            new_head.close()

            # Change value of self.head to point to the current branch -------
            self.head = self.get_head()

            new_branch = open(f"{self.repository_directory}/{self.head}", "r")
            new_branch_hash = new_branch.read()
            new_branch.close()

            print(f'Switched to branch "{name}"')

            # Update HEAD log -------
            head_log = open(f"{self.repository_directory}/logs/HEAD", "a")

            commit_time = datetime.datetime.now()
            commit_stamp = int(commit_time.timestamp())

            log_content = f"{old_branch_hash} {new_branch_hash} {self.variables['author']} {commit_stamp} switch: moving from {old_branch_name} to {name}\n"

            head_log.write(log_content)

            head_log.close()

            # TODO: Replace files of old branch with new branch files (be careful not to delete everything...again:) ) -------
            # Extract tree from commit object
            # We want the content of the new branch, because we are swapping content to the new branch
            commit_content = str(self.cat(new_branch_hash, "-p")).split("\n")

            for entry in commit_content:
                if "tree" in entry:
                    tree = entry.replace("tree ", "")
                    self.replace_repository(tree)

        else:
            print(f'"{name}" is not a branch in this repository.')

    def replace_repository(self, tree):
        # TODO: Safety feature to not mess up entire repository when switching between branches (Not really needed because each object contains it's content)
        # TODO: Find the contents of the tree
        tree_entries = str(self.cat(tree, "-p")).split("\n")

        for entry in tree_entries:
            entry_split = entry.split(" ")

            # Prevents empty entry from being processed. This is fine because the entry format is standard and doesn't change
            if len(entry_split) == 4:
                entry_dictionary = {}

                entry_dictionary["code"] = entry_split[0]
                entry_dictionary["type"] = entry_split[1]
                entry_dictionary["hash"] = entry_split[2]
                entry_dictionary["file"] = entry_split[3]

                if entry_dictionary["type"] == "blob":
                    print(
                        f"{entry_dictionary['file']} is a blob {entry_dictionary['hash']}"
                    )
                    # This overwrites files to the version in the current branch
                    for path in self.directory_files:
                        # Gives the full path for each file
                        if entry_dictionary["file"] in path:
                            # TODO: Check if overwrite was successful(get hash of file before change and compare it to hash of file after change, also compare hash to that contained in tree)
                            # To get hash before overwrite
                            old_file = open(f"{self.cwd}/{path}", "r")
                            old_file_content = old_file.read()
                            hash_before_overwrite = self.hash_object(
                                "blob", old_file_content, "-n"
                            )
                            old_file.close()

                            # To overwrite file
                            entry_content = self.cat(entry_dictionary["hash"], "-p")
                            overwrite_file = open(f"{self.cwd}/{path}", "w")

                elif entry_dictionary["type"] == "tree":
                    self.replace_repository(entry_dictionary["hash"])

        # TODO: Overwrite tree versions of the files in the directory
        # TODO: Recursively do the above for any subtrees in the main tree

    def merge(self):
        # TODO: Create a ORIG_HEAD file that contains the hash of the previous commit, before doing a potentially dangerous operation(like merging branches)
        # After merge is done, a new commit object is created with the updated files
        pass

    def get_hashes(self):
        object_path = self.cwd + "/.hvc/objects"
        object_folders = os.listdir(object_path)
        output_hashes = []

        for objects in object_folders:
            for i in os.listdir(f"{object_path}/{objects}"):
                output_hashes.append(objects + i)

        return output_hashes

    def test_hashes(self):
        for hash in self.get_hashes():
            print(f"{self.cat(hash, '-t')} {hash}")
            print(self.cat(hash, "-p"))
            print()

    # TODO: Retrieve from config files
    # Responsible for retrieving local and global hvc variables
    def get_variables(self):
        variables = {
            "author": "Hayden <email@gmail.com>",
            "commiter": "Hayden <email@gmail.com>",
            "default_branch": "master",
        }

        return variables

    def get_head(self):
        head = open(f"{self.repository_directory}/HEAD", "r")
        head_output = head.read().replace("ref: ", "")
        head_output = head_output.replace("\n", "")

        return head_output

    # Makes changes like sets default branch name or default author etc.
    def set_config(self):
        # TODO: Ask some of this information when hvc is first used
        pass

    # Check that a user given hash is a valid hash
    def hash_check(self, hash):
        pattern = "^[a-z0-9]{40}$"
        print(bool(re.search(pattern, hash)))
        return False
