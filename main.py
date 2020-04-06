#!/usr/bin/python3
import sys, json

class Application:
    def __init__(self, workload, window=None):
        self.workload = workload.data
        self.window = window if window != None else None

class Workload:
    def __init__(self, file):
        with open(file, "r") as fs:
            self.data = json.load(fs)

    def get_fixed(self):
        if "fixed" in self.data:
            return self.data["fixed"]
        else:
            return ValueError("Error: subject has no fixed field")

    def get_modules(self):
        return self.data["modules"]

class Window:
    def __init__(self):
        pass

class ArgumentHandler:
    def __init__(self, argv):
        self.argv = argv
        self.subjects = json.load(open("data/workloads.json", "r"))["workloads"]

    def check(self):
        if len(self.argv) == 1: return
        if self.argv[1] == "-m":
            if self.argv[4] not in self.subjects: return
            fs = open("data/{}.json".format(self.argv[4]), "r")
            data = json.load(fs)
            data["modules"].append({"name": "{}".format(self.argv[2]), "description": "{}".format(self.argv[3])})
            fs = open("data/{}.json".format(self.argv[4]), "w")
            json.dump(data, fs, indent=4)

        
        # elif self.argv[1] == "-f":
        #     if self.argv[4] not in self.subjects: return
        #     fs = open("data/{}.json".format(self.argv[4]), "r")
        #     if "fixed" not in fs.read(): return

        #     data = json.load(fs)           ==> throws decoding error
        
        #     data["fixed"]["{}".format(self.argv[2])] = "{}".format(self.argv[3])
        #     fs = open("data/{}.json".format(self.argv[4]), "w")
        #     json.dump(data, fs, indent=4)


h = ArgumentHandler(sys.argv)
h.check()
# w = Workload("data/medt.json")
# a = Application(w, "Hello")