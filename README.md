# Bython
Python with Braces (and constants)

The bython.bat file is a Windows command file you can place in the same folder as the core string.py file to run bython from the command line just like python- just be sure to add the command file to your environment variables for easy usage!

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

**To compile a bython file to python, you can do one of the following:**
- drag the bython file onto the command file to only compile
- run `bython "path_to_bython_file/filename.txt"` in a command line to only compile
- run `bython "path_to_bython_file/filename.txt" -e` to compile and run the file
- run `bython "path_to_bython_file/filename.txt" -e -n` in a command line to run the file and not save the compiled copy

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
- Along with the `and`, `or`, `raise`, `except`, and `elif` keywords, `&&`, `||`, `throw`, `catch`, and `else if` have also been implemented respectively
- Comments can now be declared with `//` for single line comments and `/*` to open multiline comments and `*/` to close them

# What is the `utils` package?
The `utils` contains small utilities to make Python, and by extension Bython, more user-friendly. The package adds in "hidden" types that Python has but hides from the user along with faster, more useful and user friendly, or completely new functions that work in standard Python!
- The `copy` function has been reworked to now copy entire classes, functions, and multi-dimensional lists and dictionaries, as well as featuring some new optional parameters if you don't want to take a slight performance drop with the deeper copying
- The `set` data container has been completely remade to now be a blend of the best parts of lists and dictionaries while sporting an all new look without losing any of its original functionality
- The `flatten` function has been added to take a multi-dimensional list and make it into a one-dimensional list
- The builtin `type` function has been reworked to now be *much* more useful by giving deeper type descriptions
- The builtin `isinstance` function has also bee reworked to remove that pesky `isinstance(True, int)` from returning `True` while also now checking deeper typing
- The builtin `vars` function finally has something useful to do! The function now returns a `dict` of all variables used within the function it is used on
- The `annotate` wrapper has been added to enforce deep-typing annotations on the arguments of functions as well as constant members!
- The `init` wrapper has been added to build those annoying `init` methods of classes using simple annotations and default values
- The `factory` class has been added to make using the `init` wrapper even more user-friendly by allowing unique instantiations of data containers!
- The `constants` wrapper has been added for when you want some members of a class to be constants, although the new `init` wrapper does this and more
- The `dicts` wrapper unifies the attributes and indeces of a class allowing both `instance["value"]` and `instance.value` to function identically

# Small Changes/Additions To Keep In Mind
- Python does NOT enforce constants. The compiler will throw the errors if you try to modify a constant
- Constants still need to be imported like a regular variable into other scopes using the `global` keyword and should be declared in the global scope.
- Use parentheses (`(`, `)`) around `lambda` functions
- Use parentheses (`(`, `)`) around `until` loop conditions
- Single-element dictionaries and sets must have a comma after the lone element (similar to the declaration of a single-element tuple) - this is to allow for easy `pass` blocks without using the keyword such as: `else: pass` now being written as `else {}`
- Comments are immediately removed by the compiler and can be declared with `#`, `//`, or a multiline comment starting with `/*` and closing with `*/`
- Comments CANNOT use string characters that are not escaped with `\` such as `\'` and `\"`

# Minor Bugs
- Type annotations don't work on constants.
- Type annotations, in general, can cause issues, so use them with caution. Hopefully, many should work
- As with annotations, f-strings can also cause issues
