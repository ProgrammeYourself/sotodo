#!/usr/bin/python3
import sys, os, json
from datetime import datetime
from commoncodes import CommonCode
#install with `pip3 install commoncodes`
#reference at https://mfederczuk.github.io/commoncodes/v/latest.html

DIR = "" # folder were user data is stored
CATEGORIES = "" # list of all categories

def convert_to_date(string, format):
    return datetime.strptime(string, format)

class Application:
    def __init__(self, workload, window=None):
        self.workload = workload.data
        self.window = window if window != None else None

class Workload:
    def __init__(self):
        with open(DIR+"workloads.json", "r") as fs:
            self.data = json.load(fs)

    def get_fixed(self):
        if "fixed" in self.data:
            return self.data["fixed"]
        else:
            return ValueError(2,"subject has no fixed field")

    def get_modules(self):
        return self.data["modules"]

    def get_categories(self):
        return CATEGORIES

class Window:
    def __init__(self):
        pass

class Timeline:
    def __init__(self):
        pass

def ArgumentHandler(argv):
    argc = len(argv)
    if argc == 1:
        raise CommonCode(3, "", "dir")
    if argv[1] in ["-m", "--module"]:
        path = argv[6]
        if not os.path.exists(path+"/workloads.json"):
            raise CommonCode(7, "", path, ": could not load 'workloads.json'")
        categories = json.load(open(path+"/workloads.json", "r"))["workloads"]
        if argc<7:
            raise CommonCode(3,"-m",",".join(["number","name","description","category", "directory"][len(argv)-2:]))
        elif argc>7:
            raise CommonCode(4,"-m",str(argc-6))
        elif argv[5] not in categories:
            raise CommonCode(7,"-m",argv[5],": category does not exist")
        with open("%s/%s.json"%(path, argv[5]), "r") as fs:
            data = json.load(fs)
        if "modules" not in data.keys():
            data["modules"]={argv[2]:{"name":argv[3],"desc":argv[4]}}
        else:
            data["modules"][argv[2]] = {"name":argv[3],"desc":argv[4]}
        with open("%s/%s.json"%(path, argv[5]), "w") as fs:
            json.dump(data, fs, indent="\t")
        exit(0)

    elif argv[1] in ["-f", "--fixed"]:
        path = argv[5]
        if not os.path.exists(path+"/workloads.json"):
            raise CommonCode(7, "", argv[5], ": could not load 'workloads.json'")
        categories = json.load(open(path+"/workloads.json", "r"))["workloads"]
        if argc<6:
            raise CommonCode(3,"-m",",".join(["name","date","category,", "directory"][len(argv)-2:]))
        elif argc>6:
            raise CommonCode(4,"-m",str(argc-6))
        elif argv[4] not in categories:
            raise CommonCode(7,"-f",argv[4],": category does not exist")
        with open("%s/%s.json"%(path, argv[4]), "r") as fs:
            data = json.load(fs)
        if "fixed" not in data.keys():
            data["fixed"]={argv[2]:argv[3]}
        else:
            data["fixed"][argv[2]] = argv[3]
        with open("%s/%s.json"%(path, argv[4]), "w") as fs:
            json.dump(data, fs, indent="\t")
        exit(0)

    elif argv[1] in ["-t", "--timeline"]:
        category = argv[2]
        if not os.path.exists(argv[3]):
            raise CommonCode(7, "", argv[3], ": could not find directory'")
        fixed = json.load(open(argv[3]+"/%s.json"%category, "r"))["fixed"]
        print("Timeline for ", category, ":\n")
        key_len = 0
        for k in fixed.keys():
            key_len = len(k) if len(k) > key_len else key_len
        for key, value in fixed.items():
            print(value, "|", key+(" "*(key_len-len(key))), "| in", (convert_to_date(value, "%d.%m.%Y")-datetime.now()).days, " days")
        exit()

    else:
        if not os.path.exists(argv[1]+"/workloads.json"):
            raise CommonCode(7, "", argv[1], ": could not load 'workloads.json'")
        DIR = argv[1]
        CATEGORIES = json.load(open(argv[1]+"/workloads.json", "r"))["workloads"]


ArgumentHandler(sys.argv)
w = Workload()
a = Application(w, "Hello")
