# Srikanth Chelluri
# June 2016
# Appian SAIL internal functions (a!) Sublime Text 3 snippet generator
# Note: use completions for generic functions 

import os
from os import listdir
from os.path import isfile, join
import getpass

print "Running Sublime Text 3 snippet generation (a!) for Appian SAIL..."

# Automated for Mac or PC
user = getpass.getuser()
path_sysrules = ""
if os.name == "nt":
	path_sysrules = "C:/repo/ae/bundled-apps/system/content/"
elif os.name == "posix":
	path_sysrules = "/Users/" + user + "/repo/ae/bundled-apps/system/content/"
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
	# Omit anything that's not clearly a rule
	if "SYSTEM_CONTENT" in str(file) or "SYSTEM_FOLDER" in str(file):
		continue
	# These rules have comments in their parameters
	if str(file) == "SYSTEM_SYSRULES_appdesigner_impactAnalysis_modal_controller.xml" or str(file) == "SYSTEM_SYSRULES_appdesigner_impactAnalysis_modal_view.xml":
		continue

	function = str(file[16:][:-4])
	if function == "":
		continue

	if function[0:6] != 'FOLDER':
		input_file = open(join(path_sysrules, file), 'r')
		prev_line = ""
		check_line = ""
		arg_list = [] # List of arguments for function
		type_list = [] # List of argument types for function (one-to-one mapping)
		for line in input_file:
			prev_line = check_line
			check_line = line.strip()
			if prev_line == "<namedTypedValue>":
				arg_list.append(check_line[6:][:-7])
			if prev_line == "<type>":
				type_list.append(check_line[6:][:-7])

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
		# Optional: add "a!" domain (but if user enters the domain, it may repeat, so it's left out for now - personal preference)
		if len(arg_list) == 0:
			snippet = function + "()" # With domain, snippet = "a!" + function + "()"
		elif len(arg_list) == 1:
			# One line (for clarity), highlight target AND value (less verbose)
			snippet = function + "(${1:" + arg_list[0] + ": " + type_list[0] + "})"
		elif len(arg_list) == 2:
			# One line (for clarity), highlight only values (for clarity)
			snippet = function + "(" + arg_list[0] + ": ${1:" + type_list[0] + "}, " + arg_list[1] + ": ${2:" + type_list[1] + "})"
		else:
			# Multiple lines (for clarity), highlight only values (for clarity)
			snippet = function + "(\n"
			for arg in arg_list:
				if arg_count != len(arg_list) - 1:
					snippet += "\t" + arg + ": ${" + str(arg_count + 1) + ":" + type_list[arg_count] + "},\n"
				else:
					snippet += "\t" + arg + ": ${" + str(arg_count + 1) + ":" + type_list[arg_count] + "}\n"
				arg_count += 1
			snippet += ")"
		tab_trigger = function
		description = "Appian Internal"

		snippet_count += 1
		output_file.write("<snippet>\n")
		output_file.write("\t<content><![CDATA[" + snippet + "]]></content>\n")
		output_file.write("\t<tabTrigger>" + tab_trigger + "</tabTrigger>\n")
		output_file.write("\t<scope>source.sail</scope>\n")
		output_file.write("\t<description>" + description + "</description>\n")
		output_file.write("</snippet>\n")

print str(snippet_count) + " rules processed. Exiting."