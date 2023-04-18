#!/usr/bin/python3
import os
import sys
import re

hpps = []
if len(sys.argv) < 3:
    print("invalid number of command, please specifiy [header_path] [output_path]")
    exit(1)
header_path = sys.argv[1]
output_path = sys.argv[2]
for file in os.listdir(header_path):
    if file.endswith(".hpp") or file.endswith(".h"):
        hpps.append(file)
includes = []
lines = []
defines = []
multi_line = ""
multi = True
namespaces = []
def DFS(hpps):
    dependencies = []
    seen = set()
    def travel(path):
        print(path)
        seen.add(path)
        with open(os.path.join(header_path, path), "r") as f:
            file_lines = f.readlines()
            for line in file_lines:
                m = re.search('#include "(.*)\"', line)
                if m != None:
                    new_path = m.group(1)
                    if new_path not in seen:
                        travel(new_path)
        dependencies.append(path)
    for path in hpps:
        if path not in seen:
            travel(path)
    return dependencies


right_order = DFS(hpps)
with open( output_path, "w") as dest:  
    for path in right_order:
        with open(os.path.join(header_path, path), "r") as f:
            file_lines = f.readlines()
            for line in file_lines:
                if multi_line:
                    multi_line += line
                    if not line[:-1].endswith("\\"):
                        defines.append(multi_line)
                        multi_line = ""
                        multi = False
                elif line.startswith('#include <'):
                    includes.append(line)
                elif line.startswith("#define"):

                    if line[:-1].endswith("\\"):
                        multi_line += line
                        multi = True
                    else:
                        defines.append(line)
                elif line.startswith("using namespace std"):
                    namespaces.append(line)
                elif not line.startswith("#pragma") and not  line.startswith('#include \"'):
                    lines.append(line)
    dest.write("#pragma once\n")          
    dest.writelines(set(includes))
    dest.writelines(defines)
    dest.writelines(set(namespaces))
    dest.writelines(lines)
            
