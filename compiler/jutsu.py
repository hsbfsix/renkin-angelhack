import rkparser as rkp
from sys import argv
from pprint import pprint

classRegistry = {}
notLegalCSS = ["tag"]
class RK_Class():

	def __init__(self, parsedList):
		global classRegistry
		self.name = parsedList[1]
		self.properties = {}

		if parsedList[2] == ":":
			other = classRegistry[parsedList[3]]
			for key, val in other.properties.items():
				self.properties[key] = val

			for stmt in parsedList[5]:
				if stmt[0] == "def":
					self.properties[stmt[1]] = stmt[3]
				else:
					self.properties[stmt[0]] = stmt[2]

		else:
			for stmt in parsedList[3]:
				if stmt[0] == "def":
					self.properties[stmt[1]] = stmt[3]
				else:
					self.properties[stmt[0]] = stmt[2]

		classRegistry[self.name] = self

	def __str__(self):
		st = self.name + "\n"
		for key,val in self.properties.items():
			st = st + key + " : " + val + "\n"
		return st


class RK_DOMElement():

	def __init__(self, parsedList):
		global classRegistry
		self.properties = {}
		self.children = []
		self.typeclass = parsedList[0]
		self.name = parsedList[1]

		for key, val in classRegistry[self.typeclass].properties.items():
			self.properties[key] = val

		for item in parsedList[3]:
			if item[0] in classRegistry.keys():
				self.children.append(RK_DOMElement(item))
			else:
				self.properties[item[0]] = item[2]


	def __str__(self):
		global notLegalCSS
		st = "." + self.name + " { \n"
		for key,val in self.properties.items():
			if key not in notLegalCSS:
				st = st + "    " + key + " : " + val + ";\n"
		st += "}\n"
		return st

	def gen(self, outHandle, outCSSHandle, indentLevel=0):
		outCSSHandle.write(self.__str__())
		sp = " " * (indentLevel * 4)
		if self.typeclass == "Document":
			outHandle.write(sp + "<" + self.properties["tag"] + ">\n")
			outHandle.write("<head><title>" + self.properties["title"] + "</title>\n")
			outHandle.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">\n")
			outHandle.write("</head>\n<body>\n")
		else:
			outHandle.write(sp + "<" + self.properties["tag"] + " class = \"" + self.name + "\"" + ">\n")

		for item in self.children:
			item.gen(outHandle, outCSSHandle, indentLevel + 1)

		if self.typeclass == "Document":
			outHandle.write("</body>\n")

		outHandle.write(sp + "</" + self.properties["tag"] + ">\n")


def convert(lt):
	global classRegistry
	outList = []
	for item in lt:
		if item[0] == "class":
			outList.append(RK_Class(item))
		elif item[0] in classRegistry.keys():
			outList.append(RK_DOMElement(item))
	return outList


def pr_rec(thing):
	if type(thing) is RK_DOMElement:
		print(thing)
		for item in thing.children:
			pr_rec(item)
	else:
		print(thing)


parsed = rkp.parseFile(argv[1])
outHandle = open(argv[2], "w")
outCSSHandle = open("style.css", "w")

for i in convert(parsed):
	if type(i) is RK_DOMElement:
		i.gen(outHandle, outCSSHandle)
	pr_rec(i)

