#!/usr/bin/python3
import sys, os, json
from commoncodes import CommonCode
#install with `pip3 install commoncodes`
#reference at https://mfederczuk.github.io/commoncodes/v/latest.html

DIR = "" # folder were user data is stored

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
		    return ValueError(2,"subject has no fixed field")

	def get_modules(self):
		return self.data["modules"]

class Window:
	def __init__(self):
		pass

def ArgumentHandler(argv):
    subjects = json.load(open("./data/workloads.json", "r"))["workloads"]
    argc = len(argv)
    if argc == 1:
        raise CommonCode(3, "", "dir")
    if argv[1] == "-m":
        if argc<6:
            raise CommonCode(3,"-m",",".join(["number","name","description","category"][len(argv)-2:]))
        elif argc>6:
            raise CommonCode(4,"-m",str(argc-6))
        elif argv[5] not in subjects:
            raise CommonCode(7,"-m",argv[5],": category does not exist")
        with open("data/%s.json"%argv[5], "r") as fs:
            data = json.load(fs)
        if "modules" not in data.keys():
            data["modules"]={argv[2]:{"name":argv[3],"desc":argv[4]}}
        else:
            data["modules"][argv[2]] = {"name":argv[3],"desc":argv[4]}
        with open("data/%s.json"%argv[5], "w") as fs:
            json.dump(data, fs, indent="\t")
        exit(0)

    elif argv[1] == "-f":
        if argc<5:
            raise CommonCode(3,"-m",",".join(["name","description","category"][len(argv)-2:]))
        elif argc>5:
            raise CommonCode(4,"-m",str(argc-6))
        elif argv[4] not in subjects:
            raise CommonCode(7,"-f",argv[4],": category does not exist")
        with open("data/%s.json"%argv[4], "r") as fs:
            data = json.load(fs)
        if "fixed" not in data.keys():
            data["fixed"]={argv[2]:argv[3]}
        else:
            data["fixed"][argv[2]] = argv[3]
        with open("data/%s.json"%argv[4], "w") as fs:
            json.dump(data, fs, indent="\t")
        exit(0)

    else:
        if not os.path.exists(argv[1]+"/workloads.json"):
            raise CommonCode(7, "", argv[1], ": could not find 'workloads.json'")
        DIR = argv[1]


ArgumentHandler(sys.argv)
w = Workload("data/medt.json")
a = Application(w, "Hello")
