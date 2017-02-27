import re

types = ("int", "float", "void")

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

#print("C FUNCTION REGULAR EXPRESSION MATCHER:", C_FUNC_RE)
funcMatcher = re.compile(C_FUNC_RE)
#print(funcMatcher.match("void s(int a, int b);"))

projDir = ""
outFile = "autogen.c"
JINXarg = "inStr->token"

with open(outFile, "w") as autogenC:
    autogenC.write("#include \"main.h\"\n\n") 
    autogenC.write("// Auto-generated JINX file\n")

def genJINXArgParse(argType, argPos = 0):
    return "getJINX{}(inStr, {})".format(argType, argPos)

def parseFunc(func):
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
            if (i > 0):
                autogenC.write(",")
            autogenC.write(" " + genJINXArgParse(funcArgs[i], i))
        autogenC.write(" );\n} else ")
        

with open("/home/joshua/Desktop/PROS/plutarch/include/eazzyCaller.h", "r") as headerF:
    for line in headerF:
        if (funcMatcher.match(line)):
            parseFunc(line)

with open(outFile, "a") as autogenC:
    autogenC.write(" {\n\twriteJINXMessage(\"No Match Found\");\n}")
