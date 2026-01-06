import shutil
import os


class HVC:
    # Initializes a directory as a repository
    def init(self):
        # TODO: Change template directory to config install/wherever install files go directory
        # Install script/Installation method must create the Template folder
        template_directory = "Template/"
        file_path = os.path.abspath(__file__)
        repository_directory = os.path.dirname(file_path) + "/.hvc"

        if not os.path.exists(repository_directory):
            shutil.copytree(template_directory, repository_directory)
            print(f"Initialized new HVC repository in {repository_directory}")
        else:
            print("Directory already exists.")

    def hash_object(self):
        return 0
