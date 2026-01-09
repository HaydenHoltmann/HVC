import vers_ctrl

h1 = vers_ctrl.HVC()

# h1.hash_object("blob", "what is up, doc?")

# h1.add(["main.cpp", "class.h", "class.cpp"])
# h1.add(["main.py", "vers_ctrl", "fake_file.py"])
h1.hash_object("blob", "Some other blob")
print(h1.cat("bd9dbf5aae1a3862dd1526723246b20206e5fc37", "-p"))
# print(h1.cat_content("index"))
