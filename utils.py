import builtins
import typing


class local (builtins.type, metaclass=builtins.type("local", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    '''Typing for localized variables only used as helpers within a function's scope'''
    __slots__ = tuple()


class const (builtins.list, metaclass=builtins.type("const", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    '''Typing for constant members using the 'init' decorator'''
    __slots__ = tuple()


class factory:
    '''Functional class to instantiate unqiue values for noramlly fixed values of static class variables'''
    __slots__ = ("val",)
    def __init__(self, val: typing.Any = None):
        self.val = val


class PrivateMethodError (builtins.Exception, metaclass=builtins.type("PrivateMethodError", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    '''Exception when calling a private method outside the class's scope'''
    __slots__ = tuple()


# Hidden types
dict_keys = builtins.type({}.keys())
dict_values = builtins.type({}.values())
function = builtins.type(lambda: 0)
generator = builtins.type(i for i in [])
builtin_function_or_method = builtins.type(builtins.abs)
module = builtins.type(builtins)
from io import TextIOWrapper
file = TextIOWrapper


def flatten(array: builtins.list, /) -> builtins.list:
    for i in builtins.range(builtins.len(array)):
        if builtins.isinstance(array[i], builtins.list):
            array = array[:i]+flatten(array[i])+array[i+1:]
    return array


class set(builtins.dict, metaclass=builtins.type("set", (builtins.type,), {"__repr__": lambda self: self.__name__})):
    def __init__(self: builtins.set, *args: builtins.tuple[typing.Any], duplicates: builtins.bool = False, strict: builtins.bool = False, **kwargs: builtins.dict[builtins.str, typing.Any]) -> None:
        builtins.super(set, self).__init__()
        self._strict = strict
        self._duplicates = duplicates
        for i in builtins.range(builtins.len(args if builtins.len(args) == 0 or (builtins.type(args[0]) != builtins.list and builtins.type(args[0]) != builtins.tuple) else args[0])):
            t = i
            while True:
                if t not in self:
                    self[t] = (args if builtins.len(args) == 0 or (builtins.type(args[0]) != builtins.list and builtins.type(args[0]) != builtins.tuple) else args[0])[i]
                    break
                else:
                    t += 1
        for name in kwargs:
            self[name] = kwargs[name]
        return None

    def __setattr__(self: builtins.set, name: builtins.str, value: typing.Any) -> None:
        if (not builtins.any(i is value for i in self.list()) or self._duplicates) and name not in ("_duplicates", "_strict"):
            try:
                self[name] = value
            except builtins.Exception:
                return builtins.super(set, self).__setattr__(name, value)
        elif name in ("_duplicates", "_strict"):
            return builtins.super(set, self).__setattr__(name, value)
        else:
            if self._strict:
                raise builtins.ValueError("Duplicate Value "+str(value)+" in set")
            else:
                return None

    def __getattr__(self: builtins.set, name: builtins.str) -> typing.Any:
        try:
            return self[name]
        except builtins.AttributeError:
            return builtins.super(set, self).__getattr__(name)

    def __setitem__(self: builtins.set, name: builtins.str, value: typing.Any) -> None:
        if (not builtins.any(i is value for i in self.list()) or self._duplicates) and name not in ("_duplicates", "_strict"):
            return builtins.super(set, self).__setitem__(name, value)
        elif name in ("_duplicates", "_strict"):
            return builtins.super(set, self).__setitem__(name, value)
        else:
            if self._strict:
                raise builtins.ValueError("Duplicate Value "+str(value)+" in set")
            else:
                return None

    def __getitem__(self: builtins.set, key: builtins.int, index: builtins.bool = False) -> typing.Any:
        '''
        index:
            True: Start List; Backup Dictionary
            False (Default): Start Dictionary; Backup List
        '''
        if index:
            try:
                return self.list()[key]
            except builtins.IndexError:
                try:
                    return builtins.super(set, self).__getitem__(key)
                except builtins.KeyError:
                    raise builtins.IndexError(key)
        else:
            try:
                return builtins.super(set, self).__getitem__(key)
            except builtins.KeyError:
                try:
                    return self.list()[key]
                except builtins.IndexError:
                    raise builtins.KeyError(key)

    def __repr__(self: builtins.set) -> builtins.str:
        s = "{"
        keys = builtins.list(self.keys())
        values = builtins.list(self.values())
        for i in builtins.range(builtins.len(keys)):
            if keys[i] == values[i]:
                s += (builtins.str(keys[i]) if builtins.type(keys[i]) != builtins.str else "'{}'".format(keys[i]))
            else:
                s += (builtins.str(keys[i]) if builtins.type(keys[i]) != builtins.str else "'{}'".format(keys[i]))+": "+(builtins.str(values[i]) if builtins.type(values[i]) != builtins.str else "'{}'".format(values[i]))
            s += ", "
        return s[:-2]+"}" if builtins.len(s) > 1 else "{}"

    def set(self: builtins.set) -> set:
        '''Set of Values'''
        return set(*builtins.list(self.values()))

    def dict(self: builtins.set) -> builtins.dict:
        '''Full Dictionary Output'''
        return builtins.dict(self)

    def list(self: builtins.set) -> builtins.list:
        '''List of Values'''
        return builtins.list(self.values())

    def copy(self: builtins.set, *args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> set:
        c = set(*args, **kwargs)
        for i in builtins.range(builtins.len(list(self.keys()))):
            c[builtins.list(self.keys())[i]] = builtins.list(self.values())[i]
        return c

    def append(self: builtins.set, *args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> None:
        for name in kwargs:
            self[name] = kwargs[name]
        for i in builtins.range(builtins.len(args)):
            t = i
            while True:
                if t not in self:
                    self[t] = args[i]
                    break
                else:
                    t += 1
        return None

    def count(self: builtins.set, val: typing.Any) -> builtins.int:
        return builtins.list(self.values()).count(val)

    def extend(self: builtins.set, *args: builtins.tuple[typing.Any]) -> None:
        for i in args:
            self.append(*i)
        return None

    def index(self: builtins.set, val: typing.Any) -> builtins.int:
        return builtins.list(self.keys())[builtins.list(self.values()).index(val)]

    def insert(self: builtins.set, pos: builtins.int, elmnt: typing.Any) -> None:
        if pos not in self:
            self[pos] = elmnt
        else:
            s = pos+1
            while True:
                if s in self:
                    s += 1
                else:
                    for i in builtins.range(s, pos, -1):
                        self[i] = self[i-1]
                    self[pos] = elmnt
                    break
        return None

    def remove(self: builtins.set, val: typing.Any) -> None:
        self.pop(builtins.list(self.keys())[builtins.list(self.values()).index(val)])
        return None

    def reverse(self: builtins.set) -> None:
        keys = list(self.keys())
        values = list(self.values())
        for i in builtins.range(builtins.len(keys)):
            self[keys[i]] = values[builtins.len(values)-1-i]
        return None

    @staticmethod
    def _sort(array: builtins.list) -> None:
        return builtins.sorted(builtins.list(builtins.filter(lambda i: builtins.type(i) == builtins.bool, array)))+builtins.sorted(builtins.list(builtins.filter(lambda i: builtins.type(i) == builtins.str and not i.isdigit(), array)))+builtins.sorted(builtins.list(builtins.filter(lambda i: builtins.type(i) == builtins.str and i.isdigit(), array)), key=lambda t: builtins.int(t))+builtins.sorted(builtins.list(builtins.filter(lambda i: builtins.type(i) == builtins.int or builtins.type(i) == builtins.float, array)))

    def sort(self: builtins.set) -> None:
        keys = self._sort(builtins.list(self.keys()))
        values = self._sort(builtins.list(self.values()))
        self.clear()
        for i in builtins.range(builtins.len(keys)):
            self[keys[i]] = values[i]
        return None

    def ksort(self: builtins.set) -> None:
        keys = self._sort(builtins.list(self.keys()))
        values = builtins.list(self.values())
        self.clear()
        for i in builtins.range(builtins.len(keys)):
            self[keys[i]] = values[i]
        return None

    def vsort(self: builtins.set) -> None:
        keys = list(self.keys())
        values = self._sort(builtins.list(self.values()))
        self.clear()
        for i in builtins.range(builtins.len(keys)):
            self[keys[i]] = values[i]
        return None


def copy(arg: typing.Any, /) -> typing.Any:
    '''
    Optimized copy function for speed that further attempts to clone functions and classes unlike the standard library.

    Parameters
    ----------
    arg : typing.Any
        argument to copy.

    Returns
    -------
    typing.Any
        A copy of argument arg.

    '''
    if builtins.isinstance(arg, builtins.dict):
        return builtins.type(arg)({i: copy(arg[i]) for i in arg})
    elif builtins.isinstance(arg, typing.Iterable):
        return builtins.type(arg)([copy(i) for i in arg])
    elif builtins.isinstance(arg, function):
        d = {}
        for i in builtins.dir(arg):
            try:
                d[i] = copy(arg.__getattribute__(i))
            except builtins.TypeError:
                d[i] = arg.__getattribute__(i)
        return builtins.type(arg.__name__, builtins.tuple(), d)()
    elif builtins.hasattr(arg, "__dict__") or builtins.hasattr(arg, "__slots__"):
        return builtins.type(builtins.type(arg).__name__, builtins.type(arg).__bases__, builtins.dict(copy(arg.__dict__)))()
    else:
        return arg


def type(arg: typing.Any, /, bases: builtins.tuple[builtins.type] = None, method: builtins.dict[builtins.str, function] = None) -> builtins.type:
    '''
    The deep-typing of the value passed in.

    Parameters
    ----------
    arg : typing.Any
        Value to return the deep-typing of.

    Returns
    -------
    type
        Deep-type of the value 'arg'.

    '''
    if bases == None and method == None:
        if builtins.isinstance(arg, builtins.dict):
            from types import GenericAlias
            if builtins.all(builtins.type(i) == builtins.type(builtins.list(arg.keys())[0]) for i in arg.keys()):
                t1 = builtins.type(list(arg.keys())[0])
            else:
                t1 = typing.Any
            if builtins.all(type(i) == type(builtins.list(arg.values())[0]) for i in arg.values()):
                t2 = type(list(arg.values())[0])
            else:
                t2 = typing.Any
            return GenericAlias(builtins.type(arg), (t1, t2))
        elif builtins.isinstance(arg, typing.Iterable):
            from types import GenericAlias
            if builtins.all(type(i) == type(builtins.list(arg)[0]) for i in arg):
                return GenericAlias(builtins.type(arg), type(arg[0]))
            else:
                return GenericAlias(builtins.type(arg), typing.Any)
        else:
            return builtins.type(arg)
    else:
        return builtins.type(arg, bases, method)


def isinstance(arg: typing.Any, ty: builtins.type|builtins.tuple[builtins.type], /) -> builtins.bool:
    '''
    Whether the given argument 'arg' is of type 'ty'.

    Parameters
    ----------
    arg : typing.Any
        Argument to test the typing of.
    ty : type
        Type to compare arg against.

    Returns
    -------
    bool
        Whether the arg is of type ty.

    '''
    if builtins.type(ty) == builtins.tuple:
        return builtins.any(isinstance(arg, i) for i in ty)
    else:
        if ty == typing.Any:
            return True
        if builtins.hasattr(ty, "__origin__") and builtins.hasattr(ty, "__args__"):  # GenericAlias
            if builtins.type(arg) == ty.__origin__:
                if builtins.isinstance(arg, builtins.dict) and len(ty.__args__) == 2:
                    return (builtins.all(isinstance(i, ty.__args__[0]) for i in arg.keys()) and 
                            builtins.all(isinstance(i, ty.__args__[1]) for i in arg.values()))
                else:
                    return builtins.all(isinstance(i, ty.__args__[0]) for i in arg)
            else:
                return False
        elif builtins.hasattr(ty, "__args__"):  # UnionType
            return builtins.any(isinstance(arg, i) for i in ty.__args__)
        else:
            return builtins.type(arg) == ty


def vars(func: function, /, f: builtins.bool = True, r: builtins.bool = True) -> builtins.dict[builtins.str, builtins.type]:
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
    try:
        d: builtins.dict = {i: {} for i in func.__code__.co_varnames}
        i: builtins.str
        CO_VARARGS: builtins.int = 4
        CO_VARKEYWORDS: builtins.int = 8
    
        for i in func.__annotations__:
            try:
                d[i]["type"] = func.__annotations__[i]
            except builtins.KeyError:
                pass
        try:
            for i in func.__kwdefaults__:
                d[i]["value"] = func.__kwdefaults__[i]
        except builtins.TypeError:
            pass
        if func.__code__.co_flags & CO_VARARGS and func.__code__.co_flags & CO_VARKEYWORDS:  # *args & **kwargs
            d[builtins.list(d)[-2]]["collection"] = "*"
            d[builtins.list(d)[-1]]["collection"] = "**"
        elif func.__code__.co_flags & CO_VARARGS:  # *args
            d[builtins.list(d)[-1]]["collection"] = "*"
        elif func.__code__.co_flags & CO_VARKEYWORDS:  # **kwargs
            d[builtins.list(d)[-1]]["collection"] = "**"
    
        if "return" in func.__annotations__:
            d["return"] = {}
            d["return"]["type"] = func.__annotations__["return"]
    
        for i in d:
            if "type" not in d[i]:
                d[i]["type"] = local  # typing.Any
    
        return d if not f else {
            **builtins.dict(builtins.filter(lambda i: "collection" not in i[1] and "value" not in i[1] and i[0] != "return", d.items())),
            **builtins.dict(builtins.filter(lambda i: i[1]["collection"] == "*", builtins.dict(builtins.filter(lambda i: "collection" in i[1] and "value" not in i[1] and i[0] != "return", d.items())).items())),
            **builtins.dict(builtins.filter(lambda i: "collection" not in i[1] and "value" in i[1] and i[0] != "return", d.items())),
            **builtins.dict(builtins.filter(lambda i: i[1]["collection"] == "**", builtins.dict(builtins.filter(lambda i: "collection" in i[1] and "value" not in i[1] and i[0] != "return", d.items())).items())),
            **({} if "return" not in d or not r else {"return": d["return"]})
        }
    except Exception:
        return builtins.vars(func)


def annotate(func: function, /) -> function:
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
    def wrapper(*args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> builtins.object:
        def err(name: builtins.str, ntype: builtins.str, gtype: builtins.str) -> builtins.TypeError:
            raise builtins.TypeError("Argument {} expected type '{}', got type '{}'".format(
                name, builtins.str(ntype), gtype))
        v = builtins.dict(builtins.filter(lambda i: "collection" in i[1] and "value" not in i[1] and i[0] != "return", vars(
            func, False, False).items()))
        try:
            _args = builtins.list(
                builtins.filter(lambda i: i[1]["collection"] == "*", v.items()))[0][0]
        except builtins.IndexError:
            _args = "args"
        try:
            _kwargs = builtins.list(
                builtins.filter(lambda i: i[1]["collection"] == "**", v.items()))[0][0]
        except builtins.IndexError:
            _kwargs = "kwargs"

        for i in builtins.range(builtins.len(args)):
            try:
                if i < builtins.list(func.__annotations__).index(_args):
                    if not isinstance(args[i], builtins.list(func.__annotations__.values())[i]):
                        err(builtins.list(func.__annotations__)[i],
                            (builtins.list(func.__annotations__.values())[i].__name__
                                if "[" not in builtins.str(builtins.list(func.__annotations__.values())[i]) else
                                builtins.list(func.__annotations__.values())[i]),
                            type(args[i]))
                else:
                    if not isinstance(args[i], func.__annotations__[_args]):
                        err(f"{_args} (@ index {i})",
                            (builtins.list(func.__annotations__.values())[builtins.list(func.__annotations__).index(_args)].__name__
                                if "[" not in builtins.str(builtins.list(func.__annotations__.values())[builtins.list(func.__annotations__).index(_args)]) else
                                builtins.list(func.__annotations__.values())[builtins.list(func.__annotations__).index(_args)]),
                            type(args[i]))
            except builtins.ValueError:
                if not isinstance(args[i], builtins.list(func.__annotations__.values())[i]):
                    err(builtins.list(func.__annotations__)[i],
                        (builtins.list(func.__annotations__.values())[i].__name__
                         if "[" not in builtins.str(builtins.list(func.__annotations__.values())[i]) else
                         builtins.list(func.__annotations__.values())[i]),
                        type(args[i]))
        for i in kwargs:
            if i in func.__annotations__:
                if not isinstance(kwargs[i], func.__annotations__[i]):
                    err(i,
                        (func.__annotations__[i].__name__
                         if builtins.hasattr(func.__annotations__[i], "__name__") and "[" not in builtins.str(func.__annotations__[i]) else
                         func.__annotations__[i]),
                        type(kwargs[i]))
            else:
                if not isinstance(kwargs[i], func.__annotations__[_kwargs]):
                    err(f"{_kwargs} ({i})",
                        (func.__annotations__[_kwargs].__name__
                         if builtins.hasattr(func.__annotations__[_kwargs], "__name__") and "[" not in builtins.str(func.__annotations__[_kwargs]) else
                         func.__annotations__[_kwargs]),
                        type(kwargs[i]))
        ret = func(*args, **kwargs)
        if "return" in func.__annotations__:
            if not isinstance(ret, func.__annotations__["return"]):
                err("return", func.__annotations__[
                    "return"].__name__, type(ret))
        return ret
    return wrapper


def init(cl: function, /) -> function:
    '''
    Automatically generate the '__init__' section of a class based on type annotations of the static members.
    '__strict__' can be used to turn off automatic casting. When an improper type is passed as an argument,
    having the '__strict__' property as false or omitting it completely will make python attempt to cast the
    desired type. By adding the property and assigning the value True to it, the automatic casting
    will be disabled and errors will be thrown for improper types being passed.
    
    NOTE: Do not annotate the '__strict__' property
    WARNING: Constant members are only constant during initial instantiation and are advised to be placed last

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
    def wrapper(*args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> builtins.object:
        temp = cl()
        for kwarg in kwargs:
            if kwarg in temp.__annotations__ or not builtins.hasattr(cl, "__strict__") or not cl.__strict__:
                if kwarg in temp.__annotations__ and temp.__annotations__[kwarg].__name__ == const.__name__:
                    raise builtins.TypeError(f"{kwarg!r} is a constant argument")
                temp.__setattr__(kwarg, kwargs[kwarg])
            else:
                raise builtins.TypeError(
                    f"__init__() got an unexpected keyword argument {kwarg!r}")
        for arg in builtins.range(builtins.len(args)):
            try:
                name = builtins.list(builtins.filter(lambda i: i not in builtins.list(
                    kwargs), builtins.list(temp.__annotations__)))[arg]
                if temp.__annotations__[name] == const or builtins.hasattr(temp.__annotations__[name], "__origin__") and temp.__annotations__[name].__origin__ == const:
                    raise builtins.TypeError(f"{name!r} is a constant argument")
                temp.__setattr__(name, args[arg])
            except builtins.IndexError:
                raise builtins.TypeError(f'''{cl.__name__} takes {
                    len(temp.__annotations__)
                    } positional argument{
                    's' if len(temp.__annotations__) > 1 else ''
                    } but {
                    len(args)+len(kwargs)+1
                    }''')
        for i in temp.__annotations__:
            if builtins.hasattr(temp.__annotations__[i], "__origin__") and (temp.__annotations__[i] == const or temp.__annotations__[i].__origin__ == const):
                temp.__annotations__[i] = temp.__annotations__[i].__args__[0]
            elif temp.__annotations__[i] == const:
                temp.__annotations__[i] = typing.Any
            if not builtins.hasattr(temp, i):
                raise builtins.TypeError(
                    f"{cl.__name__} missing required argument {i!r}")
            if isinstance(temp.__getattribute__(i), factory):
                temp.__setattr__(i, copy(temp.__getattribute__(i).val))
            if not isinstance(temp.__getattribute__(i), temp.__annotations__[i]):
                if builtins.hasattr(cl, "__strict__") and cl.__strict__:
                    t = type(temp.__getattribute__(i))
                    raise builtins.TypeError(f"""Argument '{i}' expected type '{
                        temp.__annotations__[i].__name__ if '[' not in str(temp.__annotations__[i]) else str(temp.__annotations__[i])
                        }', got type '{
                        t.__name__ if '[' not in str(t) else str(t)
                        }'""")
                else:
                    temp.__setattr__(i, temp.__annotations__[
                                     i](temp.__getattribute__(i)))
        return temp
    return wrapper


def constants (cl: function, /) -> function:
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
    def wrapper (*args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> builtins.object:
        def __setattr__ (self: builtins.object, attr: builtins.str, val: typing.Any) -> None:
            if (builtins.hasattr(self, attr) and builtins.hasattr(self, "__annotations__") and attr in self.__annotations__ and 
                (self.__annotations__[attr] == const or self.__annotations__[attr].__origin__ == const)):
                raise builtins.ValueError(f"Cannot reassign constant value {attr!r}")
            return builtins.super(cl2, self).__setattr__(attr, val)
        cl2 = builtins.type(cl.__name__, cl.__bases__, {**builtins.dict(cl.__dict__), "__setattr__": __setattr__})
        return cl2(*args, **kwargs)
    return wrapper


def dicts (cl: function, /) -> function:
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
    def wrapper (*args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> builtins.object:
        def __getitem__ (self, attr):
            try:
                return builtins.super(cl2, self).__getitem__(attr)
            except (builtins.AttributeError, builtins.TypeError):
                try:
                    return builtins.super(cl2, self).__getattribute__(attr)
                except (builtins.AttributeError, builtins.TypeError):
                    raise builtins.AttributeError(f"{type(self).__name__!r} object has no attribute {attr!r}")
        def __getattribute__ (self, attr):
            try:
                return builtins.super(cl2, self).__getattribute__(attr)
            except (builtins.AttributeError, builtins.TypeError):
                try:
                    return builtins.super(cl2, self).__getitem__(attr)
                except (builtins.AttributeError, builtins.TypeError):
                    raise builtins.AttributeError(f"{type(self).__name__!r} object has no attribute {attr!r}")
        cl2 = builtins.type(cl.__name__, cl.__bases__, {**builtins.dict(cl.__dict__), "__getitem__": __getitem__, "__getattribute__": __getattribute__})
        return cl2(*args, **kwargs)
    return wrapper


def private (func: function, /) -> function:
    '''
    Prevent access to method outside of the class' scope.

    Parameters
    ----------
    func : function
        Function to be decorated.

    Raises
    ------
    PrivateMethodError
        The function being called is a Private Method.

    Returns
    -------
    function
        Decorated function.

    '''
    def wrapper (*args: builtins.tuple[typing.Any], **kwargs: builtins.dict[builtins.str, typing.Any]) -> function:
        from inspect import stack
        from sys import modules
        cls = builtins.vars(modules[func.__module__])[func.__qualname__.split('.')[0]]
        caller = stack()[1].function
        if cls is wrapper:
            raise PrivateMethodError(f"{func.__name__!r} is a Private Method in the Main")
        if builtins.hasattr(cls, caller):  # not decorated class container
            return func(*args, **kwargs)
        try:
            c = cls()  # Empty init
        except Exception as e:
            c = cls(*([0]*int(str(e).split("missing")[1].split("required")[0])))  # fill with empty parameters
        if builtins.hasattr(c, caller):  # Decorated class container
            return func(*args, **kwargs)
        raise PrivateMethodError(f"{func.__name__!r} is a Private Method of class {cls.__name__!r}")
    return wrapper
