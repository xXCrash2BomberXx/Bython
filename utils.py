import builtins


class duck (builtins.type, metaclass=builtins.type("duck", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    '''Typing for variables without a strict typing class'''
    __module__ = builtins.__name__


class local (builtins.type, metaclass=builtins.type("local", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    '''Typing for localized variables only used as helpers within a function's scope'''
    __module__ = builtins.__name__


class const (list, metaclass=type("const", (type,), {"__repr__": lambda self: self.__name__})):
    '''Typing for constant static members using the 'init' decorator'''
    __module__ = builtins.__name__


class factory:
    '''Functional class to instantiate unqiue values for noramlly fixed values of static class variables'''

    def __init__(self, val: duck = None):
        self.val = val


# Hidden types
dict_keys = builtins.type({}.keys())
dict_values = builtins.type({}.values())
function = builtins.type(lambda: 0)
generator = builtins.type(i for i in [])
builtin_function_or_method = builtins.type(abs)
module = builtins.type(builtins)
from io import TextIOWrapper
file = TextIOWrapper


def flatten(array: list) -> list:
    for i in range(len(array)):
        if isinstance(array[i], list):
            array = array[:i]+flatten(array[i])+array[i+1:]
    return array


class set(dict, metaclass=type("set", (type,), {"__repr__": lambda self: self.__name__})):
    __module__ = builtins.__name__

    def __init__(self: set, *args: duck, duplicates: bool = False, strict: bool = False, **kwargs: duck) -> None:
        super(set, self).__init__()
        self._strict = strict
        self._duplicates = duplicates
        for i in range(len(args if len(args) == 0 or (type(args[0]) != list and type(args[0]) != tuple) else args[0])):
            t = i
            while True:
                if t not in self:
                    self[t] = (args if len(args) == 0 or (type(args[0]) != list and type(args[0]) != tuple) else args[0])[i]
                    break
                else:
                    t += 1
        for name in kwargs:
            self[name] = kwargs[name]
        return None

    def __setattr__(self: set, name: str, value: duck) -> None:
        if (not any(i is value for i in self.list()) or self._duplicates) and name not in ("_duplicates", "_strict"):
            try:
                self[name] = value
            except Exception:
                return super(set, self).__setattr__(name, value)
        elif name in ("_duplicates", "_strict"):
            return super(set, self).__setattr__(name, value)
        else:
            if self._strict:
                raise ValueError("Duplicate Value "+str(value)+" in set")
            else:
                return None

    def __getattr__(self: set, name: str) -> duck:
        try:
            return self[name]
        except AttributeError:
            return super(set, self).__getattr__(name)

    def __setitem__(self: set, name: str, value: duck) -> None:
        if (not any(i is value for i in self.list()) or self._duplicates) and name not in ("_duplicates", "_strict"):
            return super(set, self).__setitem__(name, value)
        elif name in ("_duplicates", "_strict"):
            return super(set, self).__setitem__(name, value)
        else:
            if self._strict:
                raise ValueError("Duplicate Value "+str(value)+" in set")
            else:
                return None

    def __getitem__(self: set, key: int, index: bool = False) -> duck:
        '''
        index:
            True: Start List; Backup Dictionary
            False (Default): Start Dictionary; Backup List
        '''
        if index:
            try:
                return self.list()[key]
            except IndexError:
                try:
                    return super(set, self).__getitem__(key)
                except KeyError:
                    raise IndexError(key)
        else:
            try:
                return super(set, self).__getitem__(key)
            except KeyError:
                try:
                    return self.list()[key]
                except IndexError:
                    raise KeyError(key)

    def __repr__(self: set) -> str:
        s = "{"
        keys = list(self.keys())
        values = list(self.values())
        for i in range(len(keys)):
            if keys[i] == values[i]:
                s += (str(keys[i]) if type(keys[i]) != str else "'{}'".format(keys[i]))
            else:
                s += (str(keys[i]) if type(keys[i]) != str else "'{}'".format(keys[i]))+": "+(str(values[i]) if type(values[i]) != str else "'{}'".format(values[i]))
            s += ", "
        return s[:-2]+"}" if len(s) > 1 else "{}"

    def set(self: set) -> set:
        '''Set of Values'''
        return set(*list(self.values()))

    def dict(self: set) -> dict:
        '''Full Dictionary Output'''
        return dict(self)

    def list(self: set) -> list:
        '''List of Values'''
        return list(self.values())

    def copy(self: set, *args: duck, **kwargs: duck) -> set:
        c = set(*args, **kwargs)
        for i in range(len(list(self.keys()))):
            c[list(self.keys())[i]] = list(self.values())[i]
        return c

    def append(self: set, *args: duck, **kwargs: duck) -> None:
        for name in kwargs:
            self[name] = kwargs[name]
        for i in range(len(args)):
            t = i
            while True:
                if t not in self:
                    self[t] = args[i]
                    break
                else:
                    t += 1
        return None

    def count(self: set, val: duck) -> int:
        return list(self.values()).count(val)

    def extend(self: set, *args: duck) -> None:
        for i in args:
            self.append(*i)
        return None

    def index(self: set, val: duck) -> int:
        return list(self.keys())[list(self.values()).index(val)]

    def insert(self: set, pos: int, elmnt: duck) -> None:
        if pos not in self:
            self[pos] = elmnt
        else:
            s = pos+1
            while True:
                if s in self:
                    s += 1
                else:
                    for i in range(s, pos, -1):
                        self[i] = self[i-1]
                    self[pos] = elmnt
                    break
        return None

    def remove(self: set, val: duck) -> None:
        self.pop(list(self.keys())[list(self.values()).index(val)])
        return None

    def reverse(self: set) -> None:
        keys = list(self.keys())
        values = list(self.values())
        for i in range(len(keys)):
            self[keys[i]] = values[len(values)-1-i]
        return None

    @staticmethod
    def _sort(array: list) -> None:
        return sorted(list(filter(lambda i: type(i) == bool, array)))+sorted(list(filter(lambda i: type(i) == str and not i.isdigit(), array)))+sorted(list(filter(lambda i: type(i) == str and i.isdigit(), array)), key=lambda t: int(t))+sorted(list(filter(lambda i: type(i) == int or type(i) == float, array)))

    def sort(self: set) -> None:
        keys = self._sort(list(self.keys()))
        values = self._sort(list(self.values()))
        self.clear()
        for i in range(len(keys)):
            self[keys[i]] = values[i]
        return None

    def ksort(self: set) -> None:
        keys = self._sort(list(self.keys()))
        values = list(self.values())
        self.clear()
        for i in range(len(keys)):
            self[keys[i]] = values[i]
        return None

    def vsort(self: set) -> None:
        keys = list(self.keys())
        values = self._sort(list(self.values()))
        self.clear()
        for i in range(len(keys)):
            self[keys[i]] = values[i]
        return None


def copy(arg: duck, trial: bool = False, quick: bool = False) -> duck:
    '''
    Optimized copy function for speed that further attempts to clone functions unlike the standard library.

    Parameters
    ----------
    arg : duck
        argument to copy.
    trial : bool, optional
        Attempt to deep-copy a function/method. The default is False.
    quick : bool, optional
        Skip deep-copying class methods. The default is False.

    Returns
    -------
    duck
        A copy of argument arg.

    '''
    if builtins.isinstance(arg, (list, set, tuple)):
        return builtins.type(arg)([copy(i) for i in arg])
    elif builtins.isinstance(arg, dict):
        return builtins.type(arg)({i: copy(arg[i]) for i in arg})
    elif builtins.isinstance(arg, function):
        if trial:
            d = {}
            for i in dir(arg):
                try:
                    d[i] = copy(arg.__getattribute__(i))
                except TypeError:
                    d[i] = arg.__getattribute__(i)
            return builtins.type(arg.__name__, tuple(), d)()
        elif not quick:
            return builtins.type(arg.__name__, tuple(), {i: arg.__getattribute__(i) for i in dir(arg)})()
        else:
            return arg
    elif hasattr(arg, "__dict__") or hasattr(arg, "__slots__"):
        return builtins.type(builtins.type(arg).__name__, builtins.type(arg).__bases__, dict(copy(arg.__dict__)))()
    else:
        return arg


def type(arg: duck, bases: tuple[builtins.type] = None, method: dict[str, function] = None) -> type:
    '''
    The deep-typing of the value passed in.

    Parameters
    ----------
    arg : duck
        Value to return the deep-typing of.

    Returns
    -------
    type
        Deep-type of the value 'arg'.

    '''
    if bases == None and method == None:
        s: str = builtins.type(arg).__name__
        if builtins.isinstance(arg, (tuple, list, set, dict)):
            try:
                if all(type(i) == type(list(arg)[0]) for i in arg):
                    temp = type(list(arg)[0])
                    s += "[" + (temp.__name__ if "[" not in str(temp)
                                else str(temp))
                else:
                    s += "[" + duck.__name__
            except IndexError:
                pass
            if builtins.isinstance(arg, dict):
                try:
                    if all(type(arg[i]) == type(arg[list(arg)[0]]) for i in arg):
                        temp = type(arg[list(arg)[0]])
                        s += ", " + \
                            (temp.__name__ if "[" not in str(
                                temp) else str(temp)) + "]"
                    else:
                        s += ", " + duck.__name__ + "]"
                except IndexError:
                    pass
            else:
                if len(arg) != 0:
                    s += "]"
            try:
                return eval(s)
            except NameError:
                return s
        else:
            try:
                return eval(s)
            except NameError:
                return s
    else:
        return builtins.type(arg, bases, method)


def isinstance(arg: duck, ty: builtins.type) -> bool:
    '''
    Whether the given argument 'arg' is of type 'ty'.

    Parameters
    ----------
    arg : duck
        Argument to test the typing of.
    ty : type
        Type to compare arg against.

    Returns
    -------
    bool
        Whether the arg is of type ty.

    '''
    try:
        if builtins.isinstance(ty, (tuple, list, set)):
            return any(isinstance(arg, t) for t in ty)
        if builtins.isinstance(ty, builtins.type):
            if "[" in str(ty):
                ty = str(ty)
            else:
                ty = ty.__name__
        ty = str(ty).replace(" ", "")
        if type(arg).__name__ == ty or ty == duck.__name__:
            return True
        elif "[" in ty and builtins.type(arg).__name__ == ty[:ty.index("[")] and len(arg) == 0:
            return True
        elif builtins.isinstance(arg, (tuple, list, set, dict)) and "[" not in ty and builtins.type(arg).__name__ == ty:
            return True
        elif builtins.isinstance(arg, (tuple, list, set)) and builtins.type(arg).__name__ == ty[:ty.index("[")]:
            if all(isinstance(i, ty[ty.index("[")+1:-1]) for i in arg):
                return True
            else:
                return False
        elif builtins.isinstance(arg, dict) and builtins.type(arg).__name__ == ty[:ty.index("[")]:
            if all(isinstance(i, ty[ty.index("[")+1:ty.index(",")]) and
                   isinstance(arg[i], ty[ty.index(",")+1:-1]) for i in arg):
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        return False


def vars(func: function, f: bool = True, r: bool = True) -> dict[str, type]:
    '''
    The variables used within the parameters and scope of the given function. 

    Parameters
    ----------
    func : function
        Function to get the variable types of.
    f : bool, optional
        Format the dictionary into a more ordered fashion. The default is True.
    r : bool, optional
        Include the return value of the function. The default is True.

    Returns
    -------
    dict[str, type]
        A dictionary containing the variables and their types within the scope of the function.

    '''
    d: dict = {i: {} for i in func.__code__.co_varnames}
    i: str
    CO_VARARGS: int = 4
    CO_VARKEYWORDS: int = 8

    for i in func.__annotations__:
        try:
            d[i]["type"] = func.__annotations__[i]
        except KeyError:
            pass
    try:
        for i in func.__kwdefaults__:
            d[i]["value"] = func.__kwdefaults__[i]
    except TypeError:
        pass
    # Has both collection arguments
    if len(list(d)) >= 3 and "value" in d[list(d)[-3]] and "value" not in d[list(d)[-2]] and "value" not in d[list(d)[-1]]:
        d[list(d)[-2]]["collection"] = "*"
        d[list(d)[-1]]["collection"] = "**"
    elif func.__code__.co_flags & CO_VARARGS:  # *args
        d[list(d)[-1]]["collection"] = "*"
    elif func.__code__.co_flags & CO_VARKEYWORDS:  # **kwargs
        d[list(d)[-1]]["collection"] = "**"
    elif "value" in d[list(d)[-1]]:  # Exclude no collection arguments
        pass
    # Exclude no keyword nor collection arguments
    elif "value" not in d[list(d)[0]]:
        pass

    if "return" in func.__annotations__:
        d["return"] = {}
        d["return"]["type"] = func.__annotations__["return"]

    for i in d:
        if "type" not in d[i]:
            d[i]["type"] = local  # duck

    return d if not f else {
        **dict(filter(lambda i: "collection" not in i[1] and "value" not in i[1] and i[0] != "return", d.items())),
        **dict(filter(lambda i: i[1]["collection"] == "*", dict(filter(lambda i: "collection" in i[1] and "value" not in i[1] and i[0] != "return", d.items())).items())),
        ** dict(filter(lambda i: "collection" not in i[1] and "value" in i[1] and i[0] != "return", d.items())),
        **dict(filter(lambda i: i[1]["collection"] == "**", dict(filter(lambda i: "collection" in i[1] and "value" not in i[1] and i[0] != "return", d.items())).items())),
        **({} if "return" not in d or not r else {"return": d["return"]})
    }


def annotate(func: function) -> function:
    '''
    Validate input into a function matches the typing annotations given.

    Parameters
    ----------
    func : function
        Function to be decorated.

    Raises
    ------
    TypeError
        The passed in arguments do not properly match the required types of the function.

    Returns
    -------
    function
        Decorated function.

    '''
    def wrapper(*args: tuple[duck], **kwargs: dict[str, duck]) -> object:
        def err(name: str, ntype: str, gtype: str) -> TypeError:
            raise TypeError("Argument {} expected type '{}', got type '{}'".format(
                name, str(ntype), gtype))
        v = dict(filter(lambda i: "collection" in i[1] and "value" not in i[1] and i[0] != "return", vars(
            func, False, False).items()))
        try:
            _args = list(
                filter(lambda i: i[1]["collection"] == "*", v.items()))[0][0]
        except IndexError:
            _args = "args"
        try:
            _kwargs = list(
                filter(lambda i: i[1]["collection"] == "**", v.items()))[0][0]
        except IndexError:
            _kwargs = "kwargs"

        for i in range(len(args)):
            try:
                if i < list(func.__annotations__).index(_args):
                    if not isinstance(args[i], list(func.__annotations__.values())[i]):
                        print(list(func.__annotations__.values())[i])
                        err(list(func.__annotations__)[i],
                            (list(func.__annotations__.values())[i].__name__
                                if "[" not in str(list(func.__annotations__.values())[i]) else
                                list(func.__annotations__.values())[i]),
                            type(args[i]))
                else:
                    if not isinstance(args[i], func.__annotations__[_args]):
                        err(f"{_args} (@ index {i})",
                            (list(func.__annotations__.values())[list(func.__annotations__).index(_args)].__name__
                                if "[" not in str(list(func.__annotations__.values())[list(func.__annotations__).index(_args)]) else
                                list(func.__annotations__.values())[list(func.__annotations__).index(_args)]),
                            type(args[i]))
            except ValueError:
                if not isinstance(args[i], list(func.__annotations__.values())[i]):
                    err(list(func.__annotations__)[i],
                        (list(func.__annotations__.values())[i].__name__
                         if "[" not in str(list(func.__annotations__.values())[i]) else
                         list(func.__annotations__.values())[i]),
                        type(args[i]))
        for i in kwargs:
            if i in func.__annotations__:
                if not isinstance(kwargs[i], func.__annotations__[i]):
                    err(i,
                        (func.__annotations__[i].__name__
                         if hasattr(func.__annotations__[i], "__name__") and "[" not in str(func.__annotations__[i]) else
                         func.__annotations__[i]),
                        type(kwargs[i]))
            else:
                if not isinstance(kwargs[i], func.__annotations__[_kwargs]):
                    err(f"{_kwargs} ({i})",
                        (func.__annotations__[_kwargs].__name__
                         if hasattr(func.__annotations__[_kwargs], "__name__") and "[" not in str(func.__annotations__[_kwargs]) else
                         func.__annotations__[_kwargs]),
                        type(kwargs[i]))
        ret = func(*args, **kwargs)
        if "return" in func.__annotations__:
            if not isinstance(ret, func.__annotations__["return"]):
                err("return", func.__annotations__[
                    "return"].__name__, type(ret))
        return ret
    return wrapper


def init(cl: function) -> function:
    '''
    Automatically generate the '__init__' section of a class based on type annotations of the static members.

    Parameters
    ----------
    cl : function
        Class to be decorated.

    Raises
    ------
    TypeError
        The passed in arguments do not properly match the required types of the function.

    Returns
    -------
    function
        Decorated class instance.

    '''
    def wrapper(*args: tuple[duck], **kwargs: dict[str, duck]) -> object:
        temp = cl()
        for kwarg in kwargs:
            if kwarg in temp.__annotations__ or not hasattr(cl, "__strict__") or not cl.__strict__:
                if kwarg in temp.__annotations__ and temp.__annotations__[kwarg].__name__ == const.__name__:
                    raise TypeError(f"{kwarg!r} is a constant argument")
                temp.__setattr__(kwarg, kwargs[kwarg])
            else:
                raise TypeError(
                    f"__init__() got an unexpected keyword argument {kwarg!r}")
        for arg in range(len(args)):
            try:
                name = list(filter(lambda i: i not in list(
                    kwargs), list(temp.__annotations__)))[arg]
                if temp.__annotations__[name].__name__ == const.__name__:
                    raise TypeError(f"{name!r} is a constant argument")
                temp.__setattr__(name, args[arg])
            except IndexError:
                raise TypeError(f'''{cl.__name__} takes {
                    len(temp.__annotations__)
                    } positional argument{
                    's' if len(temp.__annotations__) > 1 else ''
                    } but {
                    len(args)+len(kwargs)+1
                    }''')
        for i in temp.__annotations__:
            if '[' in str(temp.__annotations__[i]) and const.__name__ in str(temp.__annotations__[i]):
                temp.__annotations__[i] = eval(str(temp.__annotations__[
                                               i]).replace(const.__name__+"[", "")[:-1])
            elif temp.__annotations__[i] == const:
                temp.__annotations__[i] = duck
            if not hasattr(temp, i):
                raise TypeError(
                    f"{cl.__name__} missing required argument {i!r}")
            if isinstance(temp.__getattribute__(i), factory):
                temp.__setattr__(i, copy(temp.__getattribute__(i).val))
            if not isinstance(temp.__getattribute__(i), temp.__annotations__[i]):
                if temp.__annotations__[i].__name__ != duck.__name__:
                    if hasattr(cl, "__strict__") and cl.__strict__:
                        t = type(temp.__getattribute__(i))
                        raise TypeError(f"""Argument '{i}' expected type '{
                            temp.__annotations__[i].__name__ if '[' not in str(temp.__annotations__[i]) else str(temp.__annotations__[i])
                            }', got type '{
                            t.__name__ if '[' not in str(t) else str(t)
                            }'""")
                    else:
                        temp.__setattr__(i, temp.__annotations__[
                                         i](temp.__getattribute__(i)))
        return temp
    return wrapper


def constants (cl: function) -> function:
    '''
    Prevent modification of instance attributes marked as 'const'

    Parameters
    ----------
    cl : function
        Class to be decorated.

    Raises
    ------
    ValueError
        Cannot reassign constant value.

    Returns
    -------
    function
        Decorated class instance.

    '''
    def wrapper (*args: tuple[duck], **kwargs: dict[str, duck]) -> object:
        def __setattr__ (self: object, attr: str, val: duck) -> None:
            if hasattr(self, attr) and hasattr(self, "__annotations__") and attr in self.__annotations__ and isinstance(self.__annotations__[attr], const):
                raise ValueError(f"Cannot reassign constant value {attr!r}")
            return super(cl2, self).__setattr__(attr, val)
        cl2 = type(cl.__name__, cl.__bases__, {**dict(cl.__dict__), "__setattr__": __setattr__})
        return cl2(*args, **kwargs)
    return wrapper


def dicts (cl: function) -> function:
    '''
    Allow access of instance attributes and items interchangeably

    Parameters
    ----------
    cl : function
        Class to be decorated.

    Raises
    ------
    AttributeError
        The instance lacks the requested attribute.

    Returns
    -------
    function
        Decorated class instance.

    '''
    def wrapper (*args: tuple[duck], **kwargs: dict[str, duck]) -> object:
        def __getitem__ (self, attr):
            try:
                return super(cl2, self).__getitem__(attr)
            except (AttributeError, TypeError):
                try:
                    return super(cl2, self).__getattribute__(attr)
                except (AttributeError, TypeError):
                    raise AttributeError(f"{type(self).__name__!r} object has no attribute {attr!r}")
        def __getattribute__ (self, attr):
            try:
                return super(cl2, self).__getattribute__(attr)
            except (AttributeError, TypeError):
                try:
                    return super(cl2, self).__getitem__(attr)
                except (AttributeError, TypeError):
                    raise AttributeError(f"{type(self).__name__!r} object has no attribute {attr!r}")
        cl2 = type(cl.__name__, cl.__bases__, {**dict(cl.__dict__), "__getitem__": __getitem__, "__getattribute__": __getattribute__})
        return cl2(*args, **kwargs)
    return wrapper


if __name__ == "__main__":

    @annotate
    def test(a: duck, b: int, *args1: str, x: dict[str, list[set]] = {}, **kwargs1: bool) -> bool:
        return True

    test(1, 2, '3', '4', x={'5': [{6}]}, y=True, z=False)

    @init
    class test:
        b: bool
        i: int = 7
        l: list = factory([])
        d: const[dict] = factory({1: 2})

    x = test(1, '1', [2], x=5)
    print(type(x.i))  # NOTE: variable 'i' is automatically parsed as an int
    print(x.d)  # NOTE: the 'const' type prevents passing in of alternate values
    print(x.x)  # NOTE: the instance now has an additional member 'x'

    @init
    class test:
        __strict__ = True  # DO NOT ANNOTATE  # Prevents additional keyword arguments and auto-conversion
        b: bool
        i: int = 7
        l: list[int] = factory([])
        d: const[dict] = factory({1: 2})

    test(True, 1, [2])
    # NOTE: variables cannot be automatically parsed to different types
    # NOTE: additional members cannot be added during instantiation

    @constants
    class test:
        x: const = 1
        y: const
        z: const
        def __init__ (self, y):
            self.y = y

    x = test(2)
    # x.x = 3  # ValueError: Cannot reassign constant value 'x'
    # x.y = 3  # ValueError: Cannot reassign constant value 'y'
    x.z = 3
    # x.z = 4  # ValueError: Cannot reassign constant value 'z'

    @dicts
    class test:
        def __init__ (self, x):
            self.x = x
    
    y = test(1)
    print(y["x"], y.x)
    