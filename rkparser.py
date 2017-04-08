from pyparsing import *

### GRAMMAR ###

Comment = "--" + Regex(".*?--")
Type = Keyword("def")
DefStatement = Type + Word (alphanums + '-') + ":" + Word(alphanums)
AssignStatement = Word(alphanums + '-') + ":" + Word(alphanums)
DefStatement = Group(DefStatement | AssignStatement)
DefStatementList = Group(ZeroOrMore(DefStatement))
Inheritance = ":" + Word(alphas)
ClassDef = Keyword("class") + Word(alphas) + Optional(Inheritance) + "{" + DefStatementList + "}"
InstantiationDash = Forward()
Instantiation = Word(alphas) + Word (alphas) + "{" + Group(ZeroOrMore(Group(AssignStatement | InstantiationDash))) + "}"
InstantiationDash << Instantiation
Document = OneOrMore(Group(Comment | ClassDef | Instantiation))

def clean(obj):
	if type(obj) is tuple:
		a, _ = obj
		adash = []
		for item in a:
			adash.append(clean(item))
		a = adash
		return a
	else:
		return obj

def parseFile(fileName):
	return Document.parseFile(open(fileName, "r"))