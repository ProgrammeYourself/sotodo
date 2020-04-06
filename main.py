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
		self.subjects = json.load(open("./data/workloads.json", "r"))["workloads"]

	def check(self):
		if len(self.argv) == 1:
			return
		if self.argv[1] == "-m":
			if self.argv[4] not in self.subjects:
				return
			with open("data/%s.json"%self.argv[4], "r") as fs:
				data = json.load(fs)
			data["modules"].append({"name": self.argv[2], "description": self.argv[3]})
			with open("data/%s.json"%self.argv[4], "w") as fs:
				json.dump(data, fs, indent="\t")
		elif self.argv[1] == "-f":
			if self.argv[4] not in self.subjects:
				return
			with open("data/%s.json"%self.argv[4], "r") as fs:
				data = json.load(fs)
			if "fixed" not in data.keys():
				data["fixed"]={}
			data["fixed"][self.argv[2]] = self.argv[3]
			with open("data/%s.json"%self.argv[4], "w") as fs:
				json.dump(data, fs, indent="\t")


h = ArgumentHandler(sys.argv)
h.check()
# w = Workload("data/medt.json")
# a = Application(w, "Hello")
