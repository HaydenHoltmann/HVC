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
# h1.commit("First commit")
print(h1.cat("01b51e6ac5e39d1eb2fec3143437c6f117a58f03", "-t"))
print(h1.cat("01b51e6ac5e39d1eb2fec3143437c6f117a58f03", "-p"))
print(h1.cat("6f8a40aeb560721821e724744fd725cf777220d9", "-t"))
print(h1.cat("6f8a40aeb560721821e724744fd725cf777220d9", "-p"))
