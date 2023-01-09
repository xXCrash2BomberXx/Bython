from utils import local, isinstance, vars
import builtins

_MISSING = object()

def overload(f):
    f.__overload__ = True
    return f

class OverloadList(builtins.list):
    pass

class OverloadDict(builtins.dict):
    def __setitem__(self, key, value):
        assert builtins.isinstance(key, builtins.str), 'keys must be str'
        prior_val = self.get(key, _MISSING)
        overloaded = builtins.getattr(value, '__overload__', False)
        if prior_val is _MISSING:
            insert_val = OverloadList([value]) if overloaded else value
            super().__setitem__(key, insert_val)
        elif builtins.isinstance(prior_val, OverloadList):
            if not overloaded:
                raise builtins.ValueError(self._errmsg(key))
            prior_val.append(value)
        else:
            if overloaded:
                raise builtins.ValueError(self._errmsg(key))
            super().__setitem__(key, value)
    @staticmethod
    def _errmsg(key):
        return f'must mark all overloads with @overload: {key}'

class OverloadMeta(builtins.type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OverloadDict()
    def __new__(mcs, name, bases, namespace, **kwargs):
        overload_namespace = {
            key: Overload(val) if builtins.isinstance(val, OverloadList) else val
            for key, val in namespace.items()
        }
        return super().__new__(mcs, name, bases, overload_namespace, **kwargs)

class Overload:
    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name

    def __init__(self, overload_list):
        if not builtins.isinstance(overload_list, OverloadList):
            raise builtins.TypeError('must use OverloadList')
        if not overload_list:
            raise builtins.ValueError('empty overload list')
        self.overload_list = overload_list
        self.signatures = [vars(f) for f in overload_list]

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.overload_list!r})'

    def __get__(self, instance, _owner=None):
        if instance is None:
            return self
        return BoundOverloadDispatcher(instance, self.owner, self.name,
                                       self.overload_list, self.signatures)

    def extend(self, other):
        if not isinstance(other, Overload):
            raise builtins.TypeError
        self.overload_list.extend(other.overload_list)
        self.signatures.extend(other.signatures)

class NoMatchingOverload(builtins.Exception):
    pass

def _signature_matches(sig, bound_args):
    for name, arg in bound_args.arguments.items():
        try:
            if "collection" in sig[name]:
                if sig[name]["collection"] == "*":
                    for var in arg:
                        if not isinstance(var, sig[name]["type"]):
                            return False
                else:
                    for var in arg.values():
                        if not isinstance(var, sig[name]["type"]):
                            return False
            elif "type" in sig[name] and sig[name]["type"] != local and not isinstance(arg, sig[name]["type"]):
                return False
        except builtins.KeyError:
            pass
    return True

class BoundOverloadDispatcher:
    def __init__(self, instance, owner_cls, name, overload_list, signatures):
        self.instance = instance
        self.owner_cls = owner_cls
        self.name = name
        self.overload_list = overload_list
        self.signatures = signatures

    def best_match(self, *args, **kwargs):
        from inspect import signature
        for f, sig in builtins.zip(self.overload_list, self.signatures):
            try:
                bound_args = signature(f).bind(self.instance, *args, **kwargs)
            except builtins.TypeError:
                pass
            else:
                bound_args.apply_defaults()
                if _signature_matches(sig, bound_args):
                    return f
        raise NoMatchingOverload()
        
    def __call__(self, *args, **kwargs):
        try:
            f = self.best_match(*args, **kwargs)
        except NoMatchingOverload:
            pass
        else:
            return f(self.instance, *args, **kwargs)
        super_instance = super(self.owner_cls, self.instance)
        super_call = builtins.getattr(super_instance, self.name, _MISSING)
        if super_call is not _MISSING:
            return super_call(*args, **kwargs)
        else:
            raise NoMatchingOverload()


if __name__ == "__main__":
    
    from utils import duck

    class Test(metaclass=OverloadMeta):
        @overload
        def test(self, x: int):
            print("Passed an integer")
        @overload
        def test(self, x: str):
            print("Passed a string")
        @overload
        def test(self, x: list[int]):
            print("Passed a list of integers")
        @overload
        def test(self, x: list[str]):
            print("Passed a list of strings")
        @overload
        def test(self, x: duck):
            print("Passed other")
        @overload
        def test(self, *x: int):
            print("Passed integers")
        @overload
        def test(self, *x: duck):
            print("Passed others")
    Test().test(1)  # Passed an integer
    Test().test("")  # Passed a string
    Test().test([])  # Passed a list of integers
    Test().test([1])  # Passed a list of integers
    Test().test([""])  # Passed a list of strings
    Test().test(True)  # Passed other
    Test().test(None)  # Passed other
    Test().test(1, 2)  # Passed integers
    Test().test(True, False)  # Passed others
    