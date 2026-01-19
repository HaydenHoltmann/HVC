import vers_ctrl

h1 = vers_ctrl.HVC()

# h1.hash_object("blob", "what is up, doc?")

# h1.add(".")
# h1.add(["main.py", "vers_ctrl", "fake_file.py"])
# h1.hash_object("blob", "Some other blob")
# print()
# print(h1.cat("index", "-t"))
# print(h1.cat("index", "-p"))
# print(h1.cat("index", "-s"))
# print(h1.process_files())
h1.commit("First commit")
print(h1.test_hashes())
# print(h1.cat("9012aaf549d63e0f1698e28ef60766d7f782c27a", "-t"))
# print(h1.cat("9012aaf549d63e0f1698e28ef60766d7f782c27a", "-p"))
