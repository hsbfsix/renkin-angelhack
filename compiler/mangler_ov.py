from sys import argv
import re
from pprint import pprint

tagRegistry = {}
replacementMap = {}
validHtmlTags = ["nav", "div", "i", "img", "h1", "h2", "h3", "h4", "h5", "h6", "head", "body", "span", "button"]

htmlHandle = open(argv[1], "r")

htmlData = htmlHandle.read()

htmlOut = htmlData[:]

splitData = re.split("<|=| |>|\"|\n", htmlData)

cleanedHtmlData = []
for item in splitData:
	if item != '':
		cleanedHtmlData.append(item)

print("###################\n")
print(cleanedHtmlData)
toReplace = []
cssFiles = {}
for i, item in enumerate(cleanedHtmlData):
	if item == "class":
		j = i
		while j > (i - 10):
			j -= 1
			if cleanedHtmlData[j] in validHtmlTags:
				prefix = cleanedHtmlData[j]
				break
		else:
			continue
		target = cleanedHtmlData[i+1]
		toReplace.append((prefix, target))
	elif item == "link":
		j = i
		flag = False
		while (j < (i + 10)):
			j += 1
			if (cleanedHtmlData[j] == "text/css") | (cleanedHtmlData[j] == "stylesheet"):
				flag = True
				break
			elif (cleanedHtmlData[j] == "style") | (cleanedHtmlData[j] == "link"):
				flag = False
				break

		if flag == True:
			k = i
			while k < (i + 10):
				k += 1
				if cleanedHtmlData[k] == "href":
					cssFiles[cleanedHtmlData[k+1]] = ""
			else:
				continue


for file in cssFiles.keys():
	fileHandle = open(file, "r")
	cssFiles[file] = fileHandle.read()
	fileHandle.close()

print(toReplace)

for prefix, target in toReplace:
	replaced = ""
	if prefix in tagRegistry:
		val = tagRegistry[prefix]
		val += 1
		tagRegistry[prefix] = val
	else:
		tagRegistry[prefix] = 1

	if target in replacementMap.keys():
		replaced = replacementMap[target]
	else:
		replaced = prefix + str(tagRegistry[prefix])
		replacementMap[target] = replaced

	#htmlOut = htmlOut.replace(target, replaced)
	#htmlOut = re.sub(r"\b" + target + r"\b", replaced, htmlOut)
	#for file in cssFiles.keys():
	#	cssFiles[file] = cssFiles[file].replace(target, replaced)




print(tagRegistry)
print(cssFiles.keys())
keys = list(replacementMap.keys())
def comp(a,b):
	return len(a) - len(b)
keys.sort(key = lambda x : len(x), reverse=True)
repMap = {}
for key in keys:
	repMap[key] = replacementMap[key]

for target in repMap.keys():
	htmlOut = re.sub(r"\b" + target + r"\b", repMap[target], htmlOut)
	for file in cssFiles.keys():
		cssFiles[file] = re.sub(r"\b" + target + r"\b", repMap[target], cssFiles[file])

for file in cssFiles.keys():
	fileHandle = open(file, "w")
	fileHandle.write(cssFiles[file])
	fileHandle.close()

htmlHandle = open(argv[1], "w")
htmlHandle.write(htmlOut)
htmlHandle.close()

print(repMap)