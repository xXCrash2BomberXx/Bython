console = type('console', (), {'log': lambda *args: print(*args)})
Debug = type('Debug', (), {'log': lambda *args: print(*args)})
System = type('System', (), {'out': type('out', (), {'println': lambda *args: print(*args)})})
Console = type('Console', (), {'ReadLine': lambda *args: input(*args), 'WriteLine': lambda *args: print(*args)})
fmt = type('fmt', (), {'Println': lambda *args: print(*args)})
IO = type('IO', (), {'puts': lambda *args: print(*args), 'fwrite': lambda *args: print(*args)})
Transcript = type('Transcript', (), {'show': lambda *args: print(*args)})
raw_input = lambda *args: input(*args)
alert = lambda *args: print(*args)
prompt = lambda *args: input(*args)
print_endline = lambda *args: print(*args)
print_string = lambda *args: print(*args)
print_newline = lambda *args: print(*args)
output = lambda *args: print(*args)
input_line = lambda *args: input(*args)
read_line = lambda *args: input(*args)
DISPLAY = lambda *args: print(*args)
ShowMessage = lambda *args: print(*args)
inputbox = lambda *args: input(*args)
printf = lambda *args: print(*args)
scanf = lambda *args: input(*args)
cout = lambda *args: print(*args)
cin = lambda *args: input(*args)
CloudDeploy = lambda *args: print(*args)
Input = lambda *args: input(*args)
PRINT = lambda *args: print(*args)
INPUT = lambda *args: input(*args)
disp = lambda *args: print(*args)
puts = lambda *args: print(*args)
gets = lambda *args: input(*args)
write = lambda *args: print(*args)
writeLn = lambda *args: print(*args)
read = lambda *args: input(*args)
readLn = lambda *args: input(*args)
echo = lambda *args: print(*args)
readline = lambda *args: input(*args)
cat = lambda *args: print(*args)
dsply = lambda *args: print(*args)
display = lambda *args: print(*args)
println = lambda *args: print(*args)
readLine = lambda *args: input(*args)
getline = lambda *args: input(*args)
parseInt = lambda *args: int(*args)
parseFloat = lambda *args: float(*args)
say = lambda *args: print(*args)
ask = lambda *args: input(*args)
dialog = lambda *args: input(*args)
putStrLn = lambda *args: print(*args)
getLine = lambda *args: print(*args)
out = lambda *args, **kwargs: print(*args, *[str(i)+": "+str(kwargs[i]) for i in kwargs.keys()], end="")
log = lambda *args, **kwargs: print(*args, *[str(i)+": "+str(kwargs[i]) for i in kwargs.keys()], end=", ")
write = lambda *args, **kwargs: print(*args, *[str(i)+": "+str(kwargs[i]) for i in kwargs.keys()], end=" ")
expr = lambda *args: exec(*args)
none = None
null = None
Null = None
void = None
Void = None
true = True
false = False
t = True
f = False
typeof = type

# Compile Bython to Python
def parse (string: str) -> str:
    # Count Backslashes Before End
    def countBackslashes (string: str) -> int:
        i = len(string)-1
        count = 0
        while i in range(len(string)) and string[i] == "\\":
            count += 1
            i -= 1
        return count
    
    # Find Sub-Strings
    def parseStrings (string: str) -> list[list[int]]:
        i = 0
        o = None
        strings = []
        while i < len(string):
            if string[i] in (o if o != None else {'"', "'"}):
                if countBackslashes(string[:i])%2 == 0:
                    if o == None:
                        if (len(string) >= i+2 and string[i+1] == string[i] and string[i+2] == string[i]):
                            strings.append([i])
                            o = string[i]*3
                            i += 3
                        else:
                            o = string[i]
                            strings.append([i])
                            i += 1
                    else:
                        if (string[i:i+len(o)] == o):
                            strings[-1].append(i+1)
                            i += len(o)
                            o = None
                else:
                    i += 1
            else:
                i += 1
        return strings

    # Validates Constants
    def parseConstants (string: str, const: str = "const") -> str:
        from re import findall
        for variable in set(findall(const+r"[\s\t]*[_a-zA-Z][_a-zA-Z0-9]*(?=[\s\t]*=[^=]|[\s\t]*:=)", string)):
            if index(string, variable) != float("inf"):
                i = 0
                if len(list(filter(lambda val: val != False, 
                              [False if index(string, t, i) == float("inf") else [i:=index(string, t, i)+1, True] for t in 
                               findall(variable.replace(const, "", 1).strip()+r"(?=[\s\t]*=[^=]|[\s\t]*[\+\-\*\/\:]=)", string)]))) > 1:
                    raise ValueError(f"Cannot reassign a constant '{variable.replace(const, '', 1).strip()}'")
                else:
                    string = replace(string, variable, variable.replace(const, "", 1).strip())
        return string
    
    # Parse Increment Operators
    def parseInc (string: str) -> str:
        from re import match, search
        try:
            while True:
                i = index(string, "++")
                # ++x -> (x:=x+1)
                if i != len(string)-1 and match(r"[_a-zA-Z]", string[i+2]):
                    variable = search(r"[_a-zA-Z][_a-zA-Z0-9]*", string[i+2:]).group()
                    string = replace(string, f"++{variable}", f"({variable}:={variable}+1)")
                # x++ -> (x:=x+1)-1
                elif i != 0 and match(r"[_a-z-A-Z0-9]", string[i-1]):
                    variable = search(r"[_a-zA-Z][_a-zA-Z0-9]*", string[:i][::-1]).group()[::-1]
                    string = replace(string, f"{variable}++", f"({variable}:={variable}+1)-1")
                else:
                    raise SyntaxError("Increment Operators must be called directly on the variable being incremented")
        except (TypeError, ValueError):
            pass
        return string
    
    # Parse Decrement Operators
    def parseDec (string: str) -> str:
        from re import match, search
        try:
            while True:
                i = index(string, "--")
                # ++x -> (x:=x-1)
                if i != len(string)-1 and match(r"[_a-zA-Z]", string[i+2]):
                    variable = search(r"[_a-zA-Z][_a-zA-Z0-9]*", string[i+2:]).group()
                    string = replace(string, f"--{variable}", f"({variable}:={variable}-1)")
                # x++ -> (x:=x-1)+1
                elif i != 0 and match(r"[_a-z-A-Z0-9]", string[i-1]):
                    variable = search(r"[_a-zA-Z][_a-zA-Z0-9]*", string[:i][::-1]).group()[::-1]
                    string = replace(string, f"{variable}--", f"({variable}:={variable}-1)+1")
                else:
                    raise SyntaxError("Increment Operators must be called directly on the variable being incremented")
        except (TypeError, ValueError):
            pass
        return string
    
    # Removes Commments
    def parseComments (string: str) -> str:
        try:
            while True:
                temp = index(string, "/*")
                temp2 = index(string, "*/", temp)
                if temp != float("inf") and temp2 == float("inf"):
                    string = string[:temp]
                else:
                    string = string[:temp]+string[temp2+2:]
        except (TypeError, ValueError):
            pass
        try:
            while True:
                temp = index(string, "//")
                temp2 = index(string, "\n", temp)
                if temp != float("inf") and temp2 == float("inf"):
                    string = string[:temp]
                else:
                    string = string[:temp]+string[temp2+2:]
        except (TypeError, ValueError):
            pass
        try:
            while True:
                temp = index(string, "#")
                temp2 = index(string, "\n", temp)
                if temp != float("inf") and temp2 == float("inf"):
                    string = string[:temp]
                else:
                    string = string[:temp]+string[temp2:]
        except (TypeError, ValueError):
            pass
        return string
    
    # Index While Ignoring Sub-Strings
    def index (string: str, value: str, start: int = 0, end: int = -1):
        p = parseStrings(string)
        try:
            while True:
                start = string.index(value, start, end)
                if not any(start in range(*t) for t in p):
                    return start
                start += 1
        except (TypeError, ValueError):
            return float("inf")

    # Replace While Ignoring Sub-Strings
    def replace (string: str, old: str, new: str):
        i = 0
        try:
            while i != float("inf"):
                i = index(string, old, i)
                string = string[:i]+new+string[i+len(old):]
                i += 1
        except (TypeError, ValueError):
            return string

    # Right Index While Ignoring Sub-Strings
    def rindex (string: str, value: str, start: int = 0, end: int = -1):
        p = parseStrings(string)
        try:
            while True:
                start = string.rindex(value, start, end)
                if not any(start in range(*t) for t in p):
                    return start
                start += 1
        except (TypeError, ValueError):
            return float("inf")

    # Count Occurences While Ignoring Sub-Strings
    def count (string: str, value: str, start: int = 0, stop: int = -1):
        if start == float("inf"):
            return 0
        elif stop == float("inf"):
            stop = -1
        try:
            p = parseStrings(string)
            c = 0
            i = start
            while True:
                i = string.index(value, i, stop)
                if not any(i in range(*t) for t in p):
                    c += 1
                i += 1
        except (TypeError, ValueError):
            pass
        return c
    
    # Split While Ignoring Sub-Strings
    def split (string: str, value: str):
        try:
            p = parseStrings(string)
            l = []
            i = 0
            last_i = 0
            while True:
                i = string.index(value, i)
                if not any(i in range(*t) for t in p):
                    l.append(string[last_i:i])
                    i += 1
                    last_i = i
                else:
                    i += 1
        except (TypeError, ValueError):
            pass
        return l + [string[last_i:]]
    
    # Get Opening Brace ('{') Given Closing Index
    def getOpen (string: str, cl: int):
        if string[cl] != "}":
            raise ValueError("Opening Index is not a closing brace ('}')")
        count = -1
        while count != 0:
            p1 = rindex(string, "}", 0, cl-1)
            p2 = rindex(string, "{", 0, cl-1)
            cl = max(p1 if p1 != float("inf") else -1, 
                     p2 if p2 != float("inf") else -1)
            if cl == -1:
                raise SyntaxError()
            elif string[cl] == "{":
                count += 1
            elif string[cl] == "}":
                count -= 1
        return cl
    
    # Get Closing Brace ('}') Given Opening Index
    def getClose (string: str, op: int):
        if string[op] != "{":
            raise ValueError("Opening Index is not an opening brace ('{')")
        count = 1
        while count != 0:
            op = min(index(string, "}", op+1), index(string, "{", op+1))
            if op == float("inf"):
                raise SyntaxError()
            elif string[op] == "{":
                count += 1
            elif string[op] == "}":
                count -= 1
        return op
    
    # Replace Braces (Filtering Dictionaries and Indeces)
    def braces (string: str) -> str:
        try:
            i = 0
            while True:
                i = index(string, "{", i)
                cl = getClose(string, i)
                ind = index(string, ",", i+1, cl)
                ind2 = ind if ind != float("inf") else cl
                if (
                    # dict/set in scope
                    index(string, "{", i+1, cl) < ind or 
                    # lambda in dict
                    count(string, "{", i+1, ind2) < count(string, "}", i+1, ind2) or 
                    # index in scope
                    index(string, "[", i+1, cl) < ind or 
                    # lambda in index
                    count(string, "[", i+1, ind2) < count(string, "]", i+1, ind2) or 
                    # annotation in scope
                    index(string, "(", i+1, cl) < ind or 
                    # lambda in annotation
                    count(string, "(", i+1, ind2) < count(string, ")", i+1, ind2) or 
                    # standard scope
                    cl < ind <= index(string, ",", i+1, cl) or
                    False):
                        if (string[i:cl+1].replace("\t", "").replace("\n", "") == "{}"):
                            string = string[:i]+": pass"+string[cl+1:]
                        else:
                            r = rindex(string[:i], "\n")
                            if r == float("inf"):
                                r = 0
                            tabs = count(string[r:i], "\t")+1
                            string = (string[:i]+":"+("\n" if count(string[i+1:cl], "\n") > 1 else "")+
                            "\n".join(["\t"*tabs+i.strip(" ") for i in string[i+1:cl].split("\n")])+
                            "\n".join([i.strip(" ") for i in split(string[cl+1:], "\n")]))
                i += 1
        except (TypeError, ValueError):
            pass
        return string
    
    def extras (string: str) -> str:
        return replace(replace(replace(string, "else if", "elif"), "||", " or "), "&&", " and ")
    
    return extras(parseDec(parseInc(braces(replace(parseConstants(parseComments(replace(string, "{", "{\n"))), ";", "\n")))))

from timeit import default_timer
import ast
from copy import deepcopy

def convertExpr2Expression(Expr):
    Expr.lineno = 0
    Expr.col_offset = 0
    result = ast.Expression(Expr.value, lineno=0, col_offset = 0)
    return result

def exec_with_return(code):
    code_ast = ast.parse("\n"+code)
    init_ast = deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]
    last_ast = deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]
    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"), globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"), globals())

def console (version: str, log: bool = False) -> None:
    print(f"Bython {version}\nType \"help\", \"copyright\", \"credits\" or \"license\" for more information.")
    if log:
        with open("log.log" , "a+") as f:
            f.write(f"--Begin (v{version})--\n")
    while True:
        try:
            total = ""
            inp = input(">>> ")
            total += inp
            while inp.lower() not in ["", "quit()", "^Z"]:
                inp = input("... ")
                total += inp
            timeit = default_timer()
            if inp.lower() in ["quit()", "^z"]:
                if log:
                    with open("log.log" , "a+") as f:
                        f.write("--End--\n\n")
                break
            elif not total.strip("\n; "):
                pass
            else:
                var = exec_with_return(parse(total))
                print(f"< {var!r}")
                print(f"<< {default_timer()-timeit}s")
                if log:
                    with open("log.log" , "a+") as f:
                        f.write(f"{total}\n< {var!r}\n")
        except Exception as e:
            print(f"< {e}")
            print(f"<< {default_timer()-timeit}s")

if __name__ == "__main__":
    import sys,  os
    version = "1.0.0"
    sys.argv = [i.lower() if i[0] == "-" else i for i in sys.argv]
    if len(sys.argv) > 1:
        # bython -h | bython --help
        if any(i in sys.argv[1:] for i in ["-h", "--help"]):
            print("usage: bython [option] ... [file]\n"+
                  "-h\t: print this help message and exit (also --help)\n"+
                  "-i\t: input file to compile from (also --in, --ifile)\n"+
                  "-o\t: output file to compile to (also --out, --ofile)\n"+
                  "-n\t: do not save the compiled file (also --no-out, --nout)\n"+
                  "-e\t: run the input file after compiled (also --eval, --exec)\n"+
                  "-t\t: open the bython terminal (also --terminal, --console)\n"+
                  "-v\t: print the Bython version number and exit (also --version)\n"+
                  "-l\t: log the input and output to a file at the current directory called 'log.log' (also --log)\n"+
                  "-c\t: clear current log file in directory (also --clear)\n"+
                  "-d\t: delete current log file in directory (also --del, --delete")
            sys.exit(2)
        if any(i in sys.argv[1:] for i in ["-v", "--version"]):
            print(f"Bython {version}")
            sys.exit(2)
        if any(i in sys.argv[1:] for i in ["-c", "--clear"]):
            with open("log.log", "w+") as f:
                f.write("")
            print("Cleared Log")
        if any(i in sys.argv[1:] for i in ["-d", "--del", "--delete"]):
            if os.path.exists("log.log"):
                os.remove("log.log")
            print("Deleted Log")
        if any(i[0] != "-" for i in sys.argv[1:]) or any(i in sys.argv[1:] for i in ["-i", "--in", "--ifile", "-o", "--out", "--ofile"]):
            try:
                # bython -i in.txt
                if "-i" in sys.argv:
                    ifile = sys.argv[sys.argv.index("-i")+1]
                # bython --in in.txt
                elif "--in" in sys.argv:
                    ifile = sys.argv[sys.argv.index("--in")+1]
                # bython --ifile in.txt
                elif "--ifile" in sys.argv:
                    ifile = sys.argv[sys.argv.index("--ifile")+1]
                # bython in.txt
                elif sys.argv[1][0] != "-":
                    ifile = sys.argv[1]
                # byfile -o out.py in.txt
                else:
                    ifile = sys.argv[3]
                with open(ifile, "r") as f:
                    total = parse(f.read())
            except IndexError:
                raise FileNotFoundError("No input file specified")
            if not any(i in sys.argv[1:] for i in ["-n", "--no-out", "--nout"]):
                try:
                    # bython -i in.txt -o out.py | bython in.txt -o out.py | bython -o out.py in.txt | bython -o out.py -i in.txt
                    if "-o" in sys.argv:
                        ofile = sys.argv[sys.argv.index("-o")+1]
                    # bython -i in.txt --out out.py | bython in.txt --out out.py | bython --out out.py in.txt | bython --out out.py -i in.txt
                    elif "--out" in sys.argv:
                        ofile = sys.argv[sys.argv.index("--out")+1]
                    # bython -i in.txt --ofile out.py | bython in.txt --ofile out.py | bython --ofile out.py in.txt | bython --ofile out.py -i in.txt
                    elif "--ofile" in sys.argv:
                        ofile = sys.argv[sys.argv.index("--ofile")+1]
                    # bython in.txt out.py
                    elif len(sys.argv) > 2 and sys.argv[1][0] != "-" and sys.argv[2][0] != "-":
                        ofile = sys.argv[2]
                    # bython -i in.txt out.py
                    elif len(sys.argv) > 3 and sys.argv[1] in ["-i", "--in", "--ifile"] and sys.argv[2][0] != "-" and sys.argv[3][0] != "-":
                        ofile = sys.argv[3]
                    # bython -i in.txt
                    else:
                        ofile = os.path.splitext(ifile)[0]+".py"
                    with open(ofile, "w+") as f2:
                        f2.write(total)
                except IndexError:
                    raise FileNotFoundError("No output file specified")
            if any(i in sys.argv[1:] for i in ["-e", "--eval", "--exec", "-l", "--log"]):
                log = any(i in sys.argv[1:] for i in ["-l", "--log"])
                if log:
                    with open("log.log", "a+") as f:
                        f.write(f"--Begin (v{version})--\n")
                try:
                    timeit = default_timer()
                    var = exec_with_return(total)
                    if var != None:
                        print(f"< {var!r}")
                    print(f"<< {default_timer()-timeit}s")
                    if log:
                        with open("log.log" , "a+") as f:
                            f.write(f"{total}\n< {var!r}\n")
                except Exception as e:
                    print(f"< {e}")
                    print(f"<< {default_timer()-timeit}s")
                if log:
                    with open("log.log" , "a+") as f:
                        f.write("--End--\n\n")
            if any(i in sys.argv[1:] for i in ["-t", "--terminal", "--console"]):
                if any(i in sys.argv[1:] for i in ["-l", "--log"]):
                    console(version, log=True)
                else:
                    console(version)
        elif any(i in sys.argv[1:] for i in ["-t", "--terminal", "--console", "-l", "--log"]):
            if any(i in sys.argv[1:] for i in ["-l", "--log"]):
                console(version, log=True)
            else:
                console(version)
    else:
        console(version)
