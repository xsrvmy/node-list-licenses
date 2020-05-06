#!/usr/bin/env python3
import os
import sys
import json

cwd = os.path.dirname(os.path.realpath(__file__))

def read_package_details(folder):
    with open(os.path.join(folder, "package.json")) as f:
        j = json.load(f)
        name = j['name']
        version = j['version']
        spdx = j.get('license', 'Not specified')

    licenseTexts = []

    # check for LICENSE, NOTICE, COPYING
    for fileName in os.listdir(folder):
        if (("license" in fileName.lower() or "notice" in fileName.lower() or "copying" in fileName.lower())
            and os.path.isfile(os.path.join(folder, fileName))):
            with open(os.path.join(folder, fileName)) as f:
                licenseTexts.append((fileName, f.read()))
    return (name, version, spdx, licenseTexts)
                


if len(sys.argv) == 1:
    print("Usage: python3 main.py <node-folder> [<config>]", file=sys.stderr)
else:
    root_folder = sys.argv[1]
    if len(sys.argv) >= 3:
        config = sys.argv[2]
    else:
        config = "default.json"
    
    os.chdir(root_folder)
    os.system("npm list --json --prod > \"%s\"" % os.path.join(cwd, "tree.json"))
    os.system("npm list --parseable --prod > \"%s\"" % os.path.join(cwd, "paths.txt"))

    with open(os.path.join(cwd, "paths.txt")) as f:
        folders = f.readlines()

    output = ""


    for folder in folders:
        (name, version, spdx, licenseTexts) = read_package_details(folder.strip())
        if len(licenseTexts) == 0:
            print("Warning: package %s@%s does not seem to contain a license file" % (name, version), file=sys.stderr)
        output += "Package name: " + name + "\n"
        output += "Package version: " + version + "\n"
        if type(spdx) != type(""):
            print("Warning: package %s@%s contains deprecated license format: " % (name, version) + str(spdx), file=sys.stderr)
            output += "License field in package.json: " + json.dumps(spdx) + "\n"
        else:
            output += "SPDX identifier in package.json: " + str(spdx) + "\n"
        for (fileName, text) in licenseTexts:
            output += "Content of file %s:" % fileName + "\n"
            output += "-" * 80 + "\n"
            output += text + "\n"
            output += "-" * 80 + "\n"
        
        output += "\n" + "=" * 100 + "\n\n"

    print(output)