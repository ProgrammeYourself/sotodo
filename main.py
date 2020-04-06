#!/usr/bin/python3
import sys, json
from commoncodes import CommonCode
#install with `pip3 install commoncodes`
#reference at https://mfederczuk.github.io/commoncodes/v/latest.html

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

class ArgumentHandler:
	def __init__(self, argv):
		self.argv = argv
		self.subjects = json.load(open("./data/workloads.json", "r"))["workloads"]

	def check(self):
		argc=len(self.argv)
		if argc == 1:
			return
		if self.argv[1] == "-m":
			if argc<6:
				raise CommonCode(3,"-m",",".join(["number","name","description","category"][len(self.argv)-2:]))
			elif argc>6:
				raise CommonCode(4,"-m",str(argc-6))
			elif self.argv[5] not in self.subjects:
				raise CommonCode(7,"-m",self.argv[5],": category does not exist")
			with open("data/%s.json"%self.argv[5], "r") as fs:
				data = json.load(fs)
			if "modules" not in data.keys():
				data["modules"]={self.argv[2]:{"name":self.argv[3],"desc":self.argv[4]}}
			else:
				data["modules"][self.argv[2]] = {"name":self.argv[3],"desc":self.argv[4]}
			with open("data/%s.json"%self.argv[5], "w") as fs:
				json.dump(data, fs, indent="\t")
		elif self.argv[1] == "-f":
			if argc<5:
				raise CommonCode(3,"-m",",".join(["name","description","category"][len(self.argv)-2:]))
			elif argc>5:
				raise CommonCode(4,"-m",str(argc-6))
			elif self.argv[4] not in self.subjects:
				raise CommonCode(7,"-f",self.argv[4],": category does not exist")
			with open("data/%s.json"%self.argv[4], "r") as fs:
				data = json.load(fs)
			if "fixed" not in data.keys():
				data["fixed"]={self.argv[2]:self.argv[3]}
			else:
				data["fixed"][self.argv[2]] = self.argv[3]
			with open("data/%s.json"%self.argv[4], "w") as fs:
				json.dump(data, fs, indent="\t")
		else:
			raise CommonCode(6,self.argv[1])

h = ArgumentHandler(sys.argv)
h.check()
# w = Workload("data/medt.json")
# a = Application(w, "Hello")
