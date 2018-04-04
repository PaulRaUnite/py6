import dbm
import shelve

try:
    storage = shelve.open("data", "rw")
    print("old")
except dbm.error:
    storage = shelve.open("data", "nrw")
    print("new")

    storage["10"] = 10

    a = "a"
    storage["a1"] = list()
    storage["a2"] = list()

print(storage["10"])
print(storage["a1"] is storage["a2"])
storage.close()
