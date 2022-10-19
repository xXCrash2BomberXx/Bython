try:
    from utils import *
except ModuleNotFoundError:
    pass

import builtins

class AbstractError (builtins.Exception, metaclass=builtins.type("AbstractError", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    '''Raised when trying to instantiate an abstract class'''
    pass

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
    
    # Parse Increment Operators
    def parseInc (string: str) -> str:
        from re import match, search
        try:
            while True:
                i = index(string, "++")
                # ++x -> (x:=x+1)
                if i != len(string)-1 and match(r"[_a-zA-Z0-9]", string[i+2]):
                    variable = search(r"[_a-zA-Z0-9]*", string[i+2:]).group()
                    if variable.isnumeric() or (variable.count(".") == 1 and variable.split(".")[0].isnumeric() and variable.split(".")[1].isnumeric()):
                        string = replace(string, f"++{variable}", f"({variable}+1)")
                    else:
                        string = replace(string, f"++{variable}", f"({variable}:={variable}+1)")
                # x++ -> (x:=x+1)-1
                elif i != 0 and match(r"[_a-z-A-Z0-9]", string[i-1]):
                    variable = search(r"[_a-zA-Z0-9]*", string[:i][::-1]).group()[::-1]
                    if variable.isnumeric() or (variable.count(".") == 1 and variable.split(".")[0].isnumeric() and variable.split(".")[1].isnumeric()):
                        string = replace(string, f"{variable}++", f"({variable})")
                    else:
                        string = replace(string, f"{variable}++", f"(({variable}:={variable}+1)-1)")
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
                # --x -> (x:=x-1)
                if i != len(string)-1 and match(r"[_a-zA-Z0-9]", string[i+2]):
                    variable = search(r"[_a-zA-Z0-9]*", string[i+2:]).group()
                    if variable.isnumeric() or (variable.count(".") == 1 and variable.split(".")[0].isnumeric() and variable.split(".")[1].isnumeric()):
                        string = replace(string, f"--{variable}", f"({variable}-1)")
                    else:
                        string = replace(string, f"--{variable}", f"({variable}:={variable}-1)")
                # x-- -> (x:=x-1)+1
                elif i != 0 and match(r"[_a-z-A-Z0-9]", string[i-1]):
                    variable = search(r"[_a-zA-Z0-9]*", string[:i][::-1]).group()[::-1]
                    if variable.isnumeric() or (variable.count(".") == 1 and variable.split(".")[0].isnumeric() and variable.split(".")[1].isnumeric()):
                        string = replace(string, f"{variable}--", f"({variable})")
                    else:
                        string = replace(string, f"{variable}--", f"({variable}:={variable}-1)+1")
                else:
                    raise SyntaxError("Decrement Operators must be called directly on the variable being decremented")
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
    def index (string: str, value: str, start: int = 0, end: int = -1) -> int:
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
    def replace (string: str, old: str, new: str) -> str:
        i = 0
        try:
            while i != float("inf"):
                i = index(string, old, i)
                string = string[:i]+new+string[i+len(old):]
                i += 1
        except (TypeError, ValueError):
            return string
        
    def replaceKeyword (string: str, old: str, new: str):
        s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        i = 0
        try:
            while i != float("inf"):
                i = index(string, old, i)
                while i != float("inf") and (string[i-1] in s or string[i+len(old)] in s):    
                    i = index(string, old, i+1)
                if i == float("inf"):
                    return string
                string = string[:i]+new+string[i+len(old):]
                i += 1
        except (TypeError, ValueError):
            return string

    # Right Index While Ignoring Sub-Strings
    def rindex (string: str, value: str, start: int = 0, end: int = -1) -> int:
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
    def count (string: str, value: str, start: int = 0, stop: int = -1) -> int:
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
    def split (string: str, value: str) -> list[str]:
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
    def getOpen (string: str, cl: int) -> int:
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
    def getClose (string: str, op: int) -> int:
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
    
    # Replace Do-While loops with standard While loops
    def doWhile (string: str) -> str:
        s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        i_do = index(string, "do")
        while i_do != float("inf") and (string[i_do-1] in s or string[i_do+2] in s):
            i_do = index(string, "do", i_do)
        while i_do != float("inf"):
            i_brace = index(string, "{", i_do)
            i_close = getClose(string, i_brace)
            i_while = index(string, "\n", i_close)
            string = string[:i_do]+"\nif True {"+string[i_brace+1:i_close-1]+"\n}\n"+string[i_close+1:i_while]+string[i_brace:i_close+1]+string[i_while+1:]
            i_do = index(string, "do")
            while i_do != float("inf") and (string[i_do-1] in s or string[i_do+2] in s):
                i_do = index(string, "do", i_do)
        return string
    
    def interface (string: str) -> str:
        s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        i_interface = index(string, "interface")
        while i_interface != float("inf") and (string[i_interface-1] in s or string[i_interface+9] in s):
            i_interface = index(string, "interface", i_interface)
        while i_interface != float("inf"):
            i_close = getClose(string, index(string, "{", i_interface))
            string = string[:i_interface]+"class "+string[i_interface+9:i_close]+'\ndef __init__ (self, *args, **kwargs){raise AbstractError("Cannot instantiate abstract class")}\n'+string[i_close:]
            i_interface = index(string, "interface")
            while i_interface != float("inf") and (string[i_interface-1] in s or string[i_interface+9] in s):
                i_interface = index(string, "interface", i_interface)
        return string
    
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
                            string = (string[:i]+":"+("\n" if count(string[i+1:cl], "\n") > 1 else "")+"\n"+
                            "\n".join(["\t"*tabs+i.strip(" ") for i in string[i+1:cl].split("\n")])+"\n"+
                            "\n".join([i.strip(" ") for i in split(string[cl+1:], "\n")]))
                i += 1
        except (TypeError, ValueError):
            pass
        return string
    
    def extras (string: str) -> str:
        return replace(
            replace(
                replaceKeyword(
                    replaceKeyword(
                        replace(
                            replaceKeyword(string, "until", "while not ")
                            , "else if", "elif")
                        , "catch", "except")
                    , "throw", "raise")
                , "||", " or ")
            , "&&", " and ")
    
    string2 = ""
    while string2 != string:
        string2 = string
        string = replace(replace(string2, "\n{", "{"), " {", "{")
    
    # trim excess lines for readability
    def trim (string: str) -> str:
        i_prev_nl = 0
        i_nl = index(string, "\n")
        while i_nl != float('inf'):
            if not string[i_prev_nl:i_nl].strip():
                string = string[:i_prev_nl]+string[i_nl:]
                i_nl = index(string, "\n", i_prev_nl+1)
            else:
                i_prev_nl = i_nl
                i_nl = index(string, "\n", i_nl+1)
        return string
    
    return trim(parseDec(parseInc(braces(interface(doWhile(extras(replace(parseComments(replace(string, "{", "{\n")), ";", "\n"))))))))

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

def console (version: str, debug: bool = False) -> None:
    print(f"Bython {version}\nType \"help\", \"copyright\", \"credits\" or \"license\" for more information.")
    while True:
        try:
            total = ""
            inp = input(">>> ")
            total += inp
            while inp.lower().strip() not in ["", "quit()", "^z"]:
                inp = input("... ")
                total += inp
            timeit = default_timer()
            if inp.lower().strip() in ["quit()", "^z"]:
                return
            elif not total.strip("\n; "):
                pass
            else:
                var = exec_with_return(parse(total+"\n"))
                if var != None:
                    print(f"< {var!r}")
                    if debug:
                        print(f"<< {default_timer()-timeit}s")
        except Exception as e:
            if type(e) == EOFError:
                break
            print(f"< {e}")
            if debug:
                print(f"<< {default_timer()-timeit}s")

if __name__ == "__main__":
    import sys,  os
    version = "1.0.1"
    sys.argv = [i.lower() if i[0] == "-" else i for i in sys.argv]
    if len(sys.argv) > 1:
        # bython -h | bython --help
        if any(i in sys.argv[1:] for i in ["-h", "--help"]):
            print("usage: bython [option] ... [file]\n"+
                  "-h\t: print this help message and exit (also --help)\n"+
                  "-i\t: input file to compile from (also --in, --ifile)\n"+
                  "-c\t: output file to compile to (also -o, --compile, --out, --ofile)\n"+
                  "-d\t: display timer information of file compilation and execution (also -t, --debug, --time, --timer)\n"+
                  "-v\t: print the Bython version number and exit (also --version)\n")
        elif any(i in sys.argv[1:] for i in ["-v", "--version"]):
            print(f"Bython {version}")
        else:
            if any(i[0] != "-" for i in sys.argv[1:]) or any(i in sys.argv[1:] for i in ["-i", "--in", "--ifile"]):
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
                    else:
                        ifile = list(filter(lambda x: x[0] !="-", sys.argv[1:]))[0]
                    with open(ifile, "r") as f:
                        total = parse(f.read()+"\n")
                except IndexError:
                    raise FileNotFoundError("No input file specified")
                if any(i in sys.argv[1:] for i in ["-c", "-o", "--compile", "--out", "--ofile"]):
                    try:
                        # bython -i in.txt -c out.py | bython in.txt -c out.py | bython -c out.py -i in.txt
                        if "-c" in sys.argv:
                            ofile = sys.argv[sys.argv.index("-c")+1]
                        # bython -i in.txt -o out.py | bython in.txt -o out.py | bython -o out.py -i in.txt
                        elif "-o" in sys.argv:
                            ofile = sys.argv[sys.argv.index("-o")+1]
                        # bython -i in.txt --compile out.py | bython in.txt --compile out.py | bython --compile out.py -i in.txt
                        elif "--compile" in sys.argv:
                            ofile = sys.argv[sys.argv.index("--compile")+1]
                        # bython -i in.txt --out out.py | bython in.txt --out out.py | bython --out out.py -i in.txt
                        elif "--out" in sys.argv:
                            ofile = sys.argv[sys.argv.index("--out")+1]
                        # bython -i in.txt --ofile out.py | bython in.txt --ofile out.py | bython --ofile out.py -i in.txt
                        elif "--ofile" in sys.argv:
                            ofile = sys.argv[sys.argv.index("--ofile")+1]
                    except IndexError:
                        ofile = os.path.splitext(ifile)[0]+".py"
                    with open(ofile, "w+") as f2:
                        try:
                            with open(os.path.dirname(os.path.realpath(__file__))+r"\utils.py", "r") as f3:
                                f2.write(f3.read()+
                                         '\nimport builtins\nclass AbstractError (builtins.Exception, metaclass=builtins.type("AbstractError", (builtins.type,), {"__repr__": lambda self: self.__name__})): pass\n'+
                                         total)
                        except FileNotFoundError:
                            f2.write('import builtins\nclass AbstractError (builtins.Exception, metaclass=builtins.type("AbstractError", (builtins.type,), {"__repr__": lambda self: self.__name__})): pass\n'+total)
                try:
                    timeit = default_timer()
                    var = exec_with_return(total)
                    if var != None:
                        print(f"< {var!r}")
                    if any(i in sys.argv[1:] for i in ["-d", "-t", "--debug", "--time", "--timer"]):
                        print(f"<< {default_timer()-timeit}s")
                except Exception as e:
                    print(f"< {e}")
                    if any(i in sys.argv[1:] for i in ["-d", "-t", "--debug", "--time", "--timer"]):
                        print(f"<< {default_timer()-timeit}s")
            else:
                console(version, any(i in sys.argv[1:] for i in ["-d", "-t", "--debug", "--time", "--timer"]))
    else:
        console(version, any(i in sys.argv[1:] for i in ["-d", "-t", "--debug", "--time", "--timer"]))
        