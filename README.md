# Bython (aka Python w/ Braces)

**Regardless of the braces syntax you use, Bython has your back! Check out the following that have been tested and should work flawlessly!**
```
def example(value: T) -> T
{
    return value;
}
```
```
for value in [] {
    return value;
}
```
```
while True {
}
```
```
if True {} else {}
```

**To run a Bython file, you can do one of the following:**
- drag the bython file onto the command file
- run `bython "path_to_bython_file/filename.txt"` in a command line

More configurations can be found by running `bython -h`

# Other Major Additions
- This is bython, not python. This doesn't require indentations but you will have to use braces (`{`, `}`) and semicolons (`;`)
- Increment and Decrement operators have been added such as:
  - `++x`->`(x:=x+1)`
  - `x++`->`((x:=x+1)-1)`
  - `--x`->`(x:=x-1)`
  - `x--`->`((x:=x-1)+1)`
- Increment and Decrement operators also work with values such as:
  - `++1`->`1+1`
  - `2++`->`2`
  - `--3`->`3-1`
  - `4--`->`4`
- `until` loops have been added and function as a `while not` loop
- `do-while` loops have been added and can be used as:
    ```
    x=0;
    do {
        print(x);
        x++;
    } while x < 5;
- `for` loop standard styling from languages such as C++ has been added and can be used as:
    ```
    for (i=0; i < 5; i+=2) {
        print(i);
    }
- The `interface` class declaration has also been added for classes you don't want instantiated
- Along with the `and`, `or`, `raise`, `except`, and `elif` keywords, `&&`, `||`, `throw`, `catch`, and `else if` have also been implemented respectively
- Comments can now be declared with `//` for single line comments and `/*` to open multiline comments and `*/` to close them

# What is the `utils` package?
The `utils` contains small utilities to make Python, and by extension Bython, more user-friendly. The package adds in "hidden" types that Python has but hides from the user along with faster, more useful and user friendly, or completely new functions that work in standard Python!
- The `copy` function has been reworked to now copy entire classes, functions, and multi-dimensional lists and dictionaries, as well as featuring some new optional parameters if you don't want to take a slight performance drop with the deeper copying
- The `set` data container has been completely remade to now be a blend of the best parts of lists and dictionaries while sporting an all new look without losing any of its original functionality
- The `flatten` function has been added to take a multi-dimensional list and make it into a one-dimensional list
- The builtin `type` function has been reworked to now be *much* more useful by giving deeper type descriptions
- The builtin `isinstance` function has also bee reworked to remove that pesky `isinstance(True, int)` from returning `True` while also now checking deeper typing such as `isinstance([1, "a"], list[int|str])`
- The builtin `vars` function finally has something useful to do! The function now returns a `dict` of all variables used within the function it is used on
- The `annotate` wrapper has been added to enforce deep-typing annotations on the arguments of functions as well as constant members!
- The `init` wrapper has been added to build those annoying `init` methods of classes using simple annotations and default values
- The `factory` class has been added to make using the `init` wrapper even more user-friendly by allowing unique instantiations of data containers!
- The `constants` wrapper has been added for when you want some members of a class to be constants
- The `dicts` wrapper unifies the attributes and indeces of a class allowing both `instance["value"]` and `instance.value` to function identically
- The `private` wrapper allows Private Methods to be declared in Python by using stack checking

# Small Changes/Additions To Keep In Mind
- Use parentheses (`(`, `)`) around `lambda` functions
- Use parentheses (`(`, `)`) around `until` loop conditions
- Single-element dictionaries and sets must have a comma after the lone element (similar to the declaration of a single-element tuple) - this is to allow for easy `pass` blocks without using the keyword such as: `else: pass` now being written as `else {}`
- Comments are immediately removed by the compiler and can be declared with `#`, `//`, or a multiline comment starting with `/*` and closing with `*/`
- Comments CANNOT use string characters that are not escaped with `\` such as `\'` and `\"`

# Minor Bugs
- Type annotations, in general, can cause issues, so use them with caution. Hopefully, many should work
- As with annotations, f-strings can also cause issues
