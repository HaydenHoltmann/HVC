import shutil
import os
import hashlib
import zlib
from pathlib import Path
import re


class HVC:
    # Initializes a directory as a repository
    def __init__(self):
        self.template_directory = "Template/"
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.ignore_content = self.process_ignore()
        self.repository_directory = self.cwd + "/.hvc"
        self.objects_directory = self.repository_directory + "/objects"
        self.directory_files = self.process_files()

    def init(self):
        # TODO: Change template directory to config install/wherever install files go directory
        # Install script/Installation method must create the Template folder
        # file_path = os.path.abspath(__file__)

        if not os.path.exists(self.repository_directory):
            shutil.copytree(self.template_directory, self.repository_directory)
            print(f"Initialized new HVC repository in {self.repository_directory}")
        else:
            print("Directory already exists.")

    def hash_object(self, obj_type, content):
        header = f"{obj_type} {len(content.encode('utf-8'))}\0"

        to_hash = header + content

        # Hashing Stuff
        obj_hash = hashlib.sha1(to_hash.encode("utf-8"))

        sha1 = obj_hash.hexdigest()

        print(sha1)

        # Compression Stuff
        zlib_content = zlib.compress(to_hash.encode("utf-8"))

        # File Stuff
        if obj_type == "index":
            path = Path(".hvc/index")
            print("Index was run")
        else:
            # path = Path(".hvc/objects/" + sha1[0:2] + "/" + sha1[2:])
            path = Path(f"{self.objects_directory}/" + sha1[0:2] + "/" + sha1[2:])

        path.parent.mkdir(exist_ok=True, parents=True)

        path.write_bytes(zlib_content)

    # Add creates an index and also adds the objects to the objects folder
    def add(self, files):
        if files[0] == ".":
            # Adds all files in the repository to the index
            self.update_index("\n".join(self.directory_files))
            # Hashes and creates an object for every file in the repository
            for i in self.directory_files:
                if not os.path.isdir(i):
                    object = open(i)
                    self.hash_object("blob", object.read())
        else:
            valid_files = []
            # Checks for valid file names
            for i in range(len(files)):
                if files[i] in self.directory_files:
                    valid_files.append(files[i])
                else:
                    print(f"{files[i]} not a part of this repository")

            self.update_index("\n".join(valid_files))
            for i in valid_files:
                if not os.path.isdir(i):
                    object_valid = open(i)
                    self.hash_object("blob", object_valid.read())

    def update_index(self, files):
        self.hash_object("index", files)

    def process_ignore(self):
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

    # Creates commit objects
    def commit(self, message):
        # TODO: Can't commit if untracked changes
        # TODO: Create tree object for each directory
        print(self.directory_files)
        directories = []

        # Finds directories in repository files list
        for file in self.directory_files:
            if os.path.isdir(file):
                print(f"{file} is a directory")
                directories.append(file)

        for paths in directories:
            tree_files = []
            print(os.listdir(paths))

        # TODO: Create commit object
        # TODO: Create "master" branch file in refs
        # TODO: Create logs for tracking changes
        # TODO: Create and store last commit message in a COMMIT_EDITMSG file
        pass

    # Tracks changes to files
    def status(self):
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
            print(self.cat(hash, "-t"))
            print(self.cat(hash, "-p"))
            print()
