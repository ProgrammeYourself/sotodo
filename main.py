#!/usr/bin/python3
import sys, os, json
from datetime import datetime
from difflib import SequenceMatcher
from commoncodes import CommonCode
#install with `pip3 install commoncodes`
#reference at https://mfederczuk.github.io/commoncodes/v/latest.html

DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),"data/") # folder were user data is stored
CATEGORIES = "" # list of all categories

def convert_to_date(string, format):
    return datetime.strptime(string, format)

class Application:
    def __init__(self, workload, window=None):
        self.workload = workload.data
        self.window = window if window != None else None

class Workload:
    def __init__(self):
        with open(os.path.join(DIR,"workloads.json"), "r") as flp:
            self.data = json.load(flp)

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
    if argc==1:
        raise CommonCode(3, "", "dir")
    elif argv[1] in ["-m", "--module"]:
        if argc<7:
            raise CommonCode(3,argv[1],",".join(["number","name","description","category","directory"][argc-2:]))
        elif argc>7:
            raise CommonCode(4,argv[1],str(argc-6))
        arg  = argv[1]
        num  = argv[2]
        name = argv[3]
        desc = argv[4]
        cat  = argv[5]
        path = argv[6]
        wlp=os.path.join(path,"workloads.json")
        if not os.path.exists(wlp):
            raise CommonCode(24,wlp,"file")
        with open(wlp, "r") as wlf:
            categories = json.load(wlf)["workloads"]
        if cat not in categories:
            raise CommonCode(7,arg,cat,": category does not exist")
        with open("%s/%s.json"%(path,cat), "r") as fs:
            data = json.load(fs)
        if "modules" not in data.keys():
            data["modules"]={num:{"name":name,"desc":desc}}
        else:
            data["modules"][num] = {"name":name,"desc":desc}
        with open("%s/%s.json"%(path,cat), "w") as fs:
            json.dump(data, fs, indent="\t")
    elif argv[1] in ["-f", "--fixed"]:
        if argc<6:
            raise CommonCode(3,argv[1],",".join(["name","date","category","directory"][argc-2:]))
        elif argc>6:
            raise CommonCode(4,argv[1],str(argc-6))
        arg  = argv[1]
        name = argv[2]
        date = argv[3]
        cat  = argv[4]
        path = argv[5]
        wlp=os.path.join(path,"workloads.json")
        with open(wlp, "r") as wlf:
            categories = json.load(wlf)["workloads"]
        if cat not in categories:
            raise CommonCode(24,cat,"category")
        elif not os.path.exists(wlp):
            raise CommonCode(7, "",path, ": could not load 'workloads.json'")
        with open("%s/%s.json"%(path,cat), "r") as fs:
            data = json.load(fs)
        if "fixed" not in data.keys():
            data["fixed"]={name:date}
        else:
            data["fixed"][name] = date
        with open("%s/%s.json"%(path,cat), "w") as fs:
            json.dump(data, fs, indent="\t")
    elif argv[1] in ["-t", "--timeline"]:
        if argc<4:
            raise CommonCode(3,argv[1],",".join(["category","directory"][argc-2:]))
        elif argc>4:
            raise CommonCode(4,argv[1],str(argc-4))
        arg  = argv[1]
        cat  = argv[2]
        path = argv[3]
        categories = []
        workloads = {}
        if not os.path.exists(path):
            raise CommonCode(24,path,"directory")
        wlp = os.path.join(path,"workloads.json")
        if not os.path.exists(wlp):
            raise CommonCode(24,path,"directory")
        if cat == "all":
            if not os.path.exists(wlp):
                raise CommonCode(7, "",path, ": could not find directory'")
            with open(wlp, "r") as wlf:
                workloads = json.load(wlf)["workloads"]
            categories.extend(workloads)
        else:
            categories.append(cat)
        for c in categories:
            ignore=False
            cp=os.path.join(path,"%s.json"%c)
            try:
            	with open(cp, "r") as cf:
                    fixed = json.load(cf)["fixed"]
            except FileNotFoundError as fnfe:
                if len(categories) == 1:
                    match = False
                    with open(wlp, "r") as wlf:
	                    workloads = json.load(wlf)["workloads"]
                    for w in workloads:
                        if SequenceMatcher(None,cat, w).ratio() >= 0.5:
                            print("Unknown category: Did you mean '"+w+"' instead of '"+cat+"'?")
                            match = True
                    if not match:
                        raise fnfe
                    exit(1)
                else:
                    ignore=True

            except KeyError:
                if len(categories) == 1:
                    raise CommonCode(74, "category '%s' has no fixed field"%c)
                else:
                    ignore=True

            if not ignore:
                print("\033[1m\033[35m", c, "\033[m")
                key_len = 0
                for k in fixed.keys():
                    key_len = len(k) if len(k) > key_len else key_len
                for key, value in fixed.items():
                    print(value, "|", key+(" "*(key_len-len(key))), "| in", (convert_to_date(value, "%d.%m.%Y")-datetime.now()).days, " days")
    
    elif argv[1] in ["-c", "--check"]:
        pass

    elif argc==2:
        DIR=argv[1]
        wlp=os.path.join(DIR,"workloads.json")
        if not os.path.exists(wlp):
            raise CommonCode(7, "", DIR, ": could not load 'workloads.json'")
        with open(wlp, "r") as wlf:
	        CATEGORIES = json.load(wlf)["workloads"]


ArgumentHandler(sys.argv)
w = Workload()
a = Application(w, "Hello")
