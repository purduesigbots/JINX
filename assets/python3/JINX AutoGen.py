#!/usr/bin/env python3

import sys
import os
import tkinter
import tkinter.filedialog
import re

autoGenName = "JINXAutoGen"
types = ("int", "float", "void")

def getSubDirs(directory):
    try:
        return set(os.listdir(directory))
    except:
        return None

def isProsProj(directory):
    directories = getSubDirs(directory)
    try:
        return set(["bin", "common.mk", "firmware", "include", "Makefile", "project.pros", "src" ]).issubset(directories)
    except:
        return False

def getUserChosenDirectory():
    input("Choose a PROS project to parse- <enter> to continue")
    root = tkinter.Tk()
    root.withdraw()
    filename = tkinter.filedialog.askdirectory()
    return filename

EOL_RE = "$"	#end of line match
SOL_RE = "^"	#start of line match
ANY_RE = "."	#Any character match
WHT_RE = r"\s"	#Any whitespace match

C_IDENT_RE = "[_a-zA-Z][_a-zA-Z0-9]*"	#Valid c identifier match
C_TYPES_RE = "((unsigned" + WHT_RE + "+)?" + "(" + "|".join(types) + "))"	#Valid C type match
C_PARAM_RE = "(" + C_TYPES_RE + WHT_RE + "+" + C_IDENT_RE + ")"
C_FUNCID_RE = SOL_RE + C_PARAM_RE
C_PARAMS_RE = "((" + C_PARAM_RE + ")?(, " + C_PARAM_RE + ")*)"
C_FUNC_RE = C_FUNCID_RE + WHT_RE + r"*\(" + C_PARAMS_RE + "\);"

print("C FUNCTION REGULAR EXPRESSION MATCHER:", C_FUNC_RE)
funcMatcher = re.compile(C_FUNC_RE)
#print(funcMatcher.match("void s(int a, int b);"))

projDir = ""
outFile = "autogen.c"
JINXarg = "inStr->token"

def startAutoGen(outFile):
    with open(outFile, "w") as autogenC:
        autogenC.write("#include \"main.h\"\n")
        autogenC.write("#include \"JINX.h\"\n\n")
        autogenC.write("// Auto-generated JINX file\n\n")
        autogenC.write("void autoJINXparse(JINX *inStr) {\n")

def genJINXArgParse(argType, argPos = 0):
    return "getJINX{}(inStr, {})".format(argType, argPos + 1)

def parseFunc(func, outFile):
    funcName = func[0:func.find("(")].strip().split()
    funcRet = "_".join(funcName[0:-1])
    funcName = funcName[-1]
    #print(funcRet, funcName, end = " ")
    
    funcArgs = func[func.find("(") + 1: func.find(")")].strip().split(",")
    #print(funcArgs)
    for i in range(len(funcArgs)):
        funcArgs[i] = "_".join(funcArgs[i].strip().split()[:-1])
    #print(funcArgs)
    with open(outFile, "a") as autogenC:
        autogenC.write("if (strcmp(\"{}\", {}) == 0) {{\n".format(funcName, JINXarg))
        autogenC.write("\t{}(".format(funcName))
        for i in range(len(funcArgs)):
            if (not funcArgs[i]):
                continue
            if (i > 0):
                autogenC.write(",")
            autogenC.write(" " + genJINXArgParse(funcArgs[i], i))
        autogenC.write(" );\n} else ")

def parseHeader(headerFile, outFile):
    with open(headerFile, "r") as headerF:
        for line in headerF:
            if (funcMatcher.match(line)):
                parseFunc(line, outFile)

def endAutoGen(outFile):
    with open(outFile, "a") as autogenC:
        autogenC.write(" {\n\twriteJINXMessage(\"No Match Found\");\n}\n}")

def parseHeaders(prosProj, outFile):
    headerPath  = os.path.join(prosProj, "include") + os.sep
    #print(headerPath)
    hFiles = [file for file in os.listdir(headerPath) if os.path.isfile(os.path.join(headerPath, file)) and file.endswith(".h")]
    #print(hFiles)
    for file in hFiles:
        file = os.path.join(headerPath, file)
        parseHeader(file, outFile)


if (__name__ == "__main__"):
    dir = getUserChosenDirectory()
    if not isProsProj(dir):
        print("Not a valid PROS project...")
        sys.exit(1)
    autoGenFile = os.path.join(dir, "src", "JINXAutoGen.c")
    startAutoGen(autoGenFile)
    parseHeaders(dir, autoGenFile)
    endAutoGen(autoGenFile)
