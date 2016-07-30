# Srikanth Chelluri, Mathew Jennings
# June 2016
# Appian SAIL internal functions (fn!) Sublime Text 3 snippet generator
# Note: use completions for generic functions 

import os
from os import listdir
from os.path import isfile, join
import getpass
import sys

print "Running Sublime Text 3 snippet generation (fn!) for Appian SAIL..."

# Automated for Mac or PC
user = getpass.getuser()
path_sysrules = ""
if os.name == "nt":
	path_sysrules = "C:/repo/ae/appian-functions/src/main/resources/appian/system/scripting-functions/"
elif os.name == "posix":
	path_sysrules = "/Users/" + user + "/repo/ae/appian-functions/src/main/resources/appian/system/scripting-functions/"
else:
	print("Not compatible with OS. Exiting.")
	exit()

try:
	dirs = [f for f in listdir(path_sysrules) if isfile(join(path_sysrules, f))]
except:
	print("Can't find directory. In Windows, 'repo' should be in C:/. In Mac OS X, 'repo' should be in /Users/" + user + "/. Exiting.")
	exit()

snippet_count = 0

for file in dirs:
	function = str(file[:-17])
	if function == "suggest-functions" or function == "processmodelmetrics" : # TODO: handle special cases
		continue
	if function == "resource_appian_internal": # Document does not need to be parsed
		continue
	if function == "":
		continue

	arg_list = [] # List of arguments for function
	input_file = open(join(path_sysrules, file), 'r')
	for line in input_file:
		if ".param" not in line:
			continue
		param_index = line.index(".param", 8) # Start after 'function.' in line
		param_index += 1
		# print(line[param_index:])
		start_index = line[param_index:].index(".") + param_index + 1
		rest_line = line[start_index:]
		end_index = start_index
		period_index = sys.maxint
		equals_index = sys.maxint
		if "." in rest_line:
			period_index = rest_line.index(".") + start_index
		if "=" in rest_line:
			equals_index = rest_line.index("=") + start_index
		end_index = min(period_index, equals_index)
		arg_list.append(line[start_index:end_index])

	output_file = ""
	if os.name == "posix":
		if not os.path.exists("/Users/" + user + "/Library/Application Support/Sublime Text 3/Packages/User/sail-snippets/"):
			os.makedirs("/Users/" + user + "/Library/Application Support/Sublime Text 3/Packages/User/sail-snippets/")
		output_file = open("/Users/" + user + "/Library/Application Support/Sublime Text 3/Packages/User/sail-snippets/" + function + ".sublime-snippet", 'w')
	else:
		if not os.path.exists("C:/Users/" + user + "/AppData/Roaming/Sublime Text 3/Packages/User/sail-snippets/"):
			os.makedirs("C:/Users/" + user + "/AppData/Roaming/Sublime Text 3/Packages/User/sail-snippets/")
		output_file = open("C:/Users/" + user + "/AppData/Roaming/Sublime Text 3/Packages/User/sail-snippets/" + function + ".sublime-snippet", 'w')
		
	arg_count = 0

	snippet = ""
	# Optional: add "fn!" domain (but if user enters the domain, it may repeat, so it's left out for now - personal preference)
	if len(arg_list) == 0:
		snippet = function + "()" # With domain, snippet = "a!" + function + "()"
	elif len(arg_list) == 1:
		# One line (for clarity), highlight target AND value (less verbose)
		snippet = function + "(${1:" + arg_list[0] + "})"
	elif len(arg_list) == 2:
		# One line (for clarity), highlight only values (for clarity)
		snippet = function + "(${1:" + arg_list[0] + "}, ${2:" + arg_list[1] + "})"
	else:
		# Multiple lines (for clarity), highlight only values (for clarity)
		snippet = function + "(\n"
		for arg in arg_list:
			if arg_count != len(arg_list) - 1:
				snippet += "\t${" + str(arg_count + 1) + ":" + arg_list[arg_count] + "},\n"
			else:
				snippet += "\t${" + str(arg_count + 1) + ":" + arg_list[arg_count] + "}\n"
			arg_count += 1
		snippet += ")"
	tab_trigger = function
	description = "Internal (plugin)"

	snippet_count += 1
	output_file.write("<snippet>\n")
	output_file.write("\t<content><![CDATA[" + snippet + "]]></content>\n")
	output_file.write("\t<tabTrigger>" + tab_trigger + "</tabTrigger>\n")
	output_file.write("\t<scope>source.sail</scope>\n")
	output_file.write("\t<description>" + description + "</description>\n")
	output_file.write("</snippet>\n")

print str(snippet_count) + " internal functions processed. Exiting."
