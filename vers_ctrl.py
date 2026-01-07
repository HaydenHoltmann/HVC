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

        print(self.ignore_content[0])
        print(self.ignore_content[1])

        self.directory_files = [
            x
            for x in os.listdir(self.cwd)
            if x not in self.ignore_content[0] not in self.ignore_content[1]
        ]
        # os.listdir(self.cwd)

    def init(self):
        # TODO: Change template directory to config install/wherever install files go directory
        # Install script/Installation method must create the Template folder
        file_path = os.path.abspath(__file__)
        repository_directory = self.cwd + "/.hvc"

        if not os.path.exists(repository_directory):
            shutil.copytree(self.template_directory, repository_directory)
            print(f"Initialized new HVC repository in {repository_directory}")
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
        path = Path(".hvc/objects/" + sha1[0:2] + "/" + sha1[2:])

        path.parent.mkdir(exist_ok=True, parents=True)

        path.write_bytes(zlib_content)

    def add(self, files):
        if files[0] == ".":
            print(self.directory_files)
        else:
            print(self.cwd)

    def update_index(self):
        hello = "hello"

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
