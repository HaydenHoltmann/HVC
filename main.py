import vers_ctrl

h1 = vers_ctrl.HVC()

# h1.hash_object("blob", "what is up, doc?")

# h1.add(".")
# h1.add(["main.py", "vers_ctrl", "fake_file.py"])
# h1.hash_object("blob", "Some other blob")
# print(h1.cat_content("index"))
print(h1.process_files())
