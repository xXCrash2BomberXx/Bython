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
# Major Changes
**Minor Bugs:**
- Type annotations don't work on constants.
- Type annotations, in general, can cause issues, so use them with caution. Hopefully, many should work
- As with annotations, f-strings can also cause issues

**Language Changes to keep in mind:**
- This is bython, not python. This doesn't require indentations but you will have to use braces (`{`, `}`) and semicolons (`;`)
- Python does NOT enforce constants. The compiler will throw the errors if you try to modify a constant
- Constants still need to be imported like a regular variable into other scopes using the `global` keyword and should be declared in the global scope.
- Use parentheses (`(`, `)`) around lambda functions
- Single-element dictionaries and sets must have a comma after the lone element (similar to the declaration of a single-element tuple) - this is to allow for easy `pass` blocks without using the keyword such as: `else: pass` now being written as `else {}`
- Comments are immediately removed by the compiler and can be declared with `#`, `//`, or a multiline comment starting with `/*` and closing with `*/`
- Comments CANNOT use string characters that are not escaped with `\` such as `\'` and `\"`
- Along with the `and` and `or` keywords, `&&` and `||` have also been implemented respectively
- Increment and Decrement operators have been added such as: `++x`, `x++`, `--x`, and `x--`
