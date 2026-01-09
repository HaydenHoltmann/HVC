import shutil
import os
import hashlib
import zlib
from pathlib import Path


class HVC:
    # Initializes a directory as a repository
    def __init__(self):
        self.template_directory = "Template/"
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.ignore_content = self.process_ignore()
        self.repository_directory = self.cwd + "/.hvc"
        self.objects_directory = self.repository_directory + "/objects"

        directories_ignored = [
            x for x in os.listdir(self.cwd) if x not in self.ignore_content[0]
        ]

        self.directory_files = [
            x for x in directories_ignored if x not in self.ignore_content[1]
        ]

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

    def add(self, files):
        if files[0] == ".":
            # Adds all files/directories in the repository to the index
            self.update_index(self.directory_files)
        else:
            valid_files = []
            # Checks for valid file names
            for i in range(len(files)):
                if files[i] in self.directory_files:
                    valid_files.append(files[i])
                else:
                    print(f"{files[i]} not a part of this repository")

            self.update_index(files)

    def update_index(self, files):
        self.hash_object("index", "Different stuff")

    def process_ignore(self):
        ignore_file = open(".hvc_ignore")
        ignore_output = []
        ignore_files = []
        ignore_directories = []

        # TODO: Add support for things like file types etc. that need to be in an ignore file. You might have to separate into different lists
        for line in ignore_file:
            if line[0] == "#" or line == " " or line == "\n":
                pass
            elif line[0] == "/":
                ignore_directories.append(line[1 : len(line) - 1])
            else:
                ignore_files.append(line[: len(line) - 1])

        ignore_output.append(ignore_directories)
        ignore_output.append(ignore_files)

        ignore_file.close()

        return ignore_output

    # Returns the content of a compressed object file(including index)
    def cat_content(self, hash):
        if hash == "index":
            hashed_file = open(f"{self.repository_directory}/index", "rb")

        else:
            hash_folder = hash[:2]
            hash_file = hash[2:]

            hashed_file = open(
                f"{self.objects_directory}/{hash_folder}/{hash_file}", "rb"
            )

        toUnhash = hashed_file.read()

        unhashed_content = zlib.decompress(toUnhash)
        unhashed_split = unhashed_content.split(b"\0")

        content_output = unhashed_split[1].decode("utf-8")

        return content_output

    # Returns the type of an object file
    def cat_type(self, hash):
        pass
