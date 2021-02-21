# Help

[Python TypeError: ‘module’ object is not callable Solution](https://careerkarma.com/blog/python-typeerror-module-object-is-not-callable/)

## Module

Python Modules are stored in /lib/site-packages in your Python folder.  
If you want to see what directories Python checks when importing modules, you can log the following:

````python
import sys
modulepath = sys.path
for item in modulepath:
	print(item)
````

## Import from Module directory

````python
import sys
version = sys.getwindowsversion()
print(f'Windows {str(version.major)}.{str(version.minor)}, Build {version.build}')
````

## Import from other directory

````python
import sys
sys.path.append('D:\DevOps\github.com\learningPython\Modules')
import PyNetTools

# Colors
W  = '\033[0m'  # white (normal)
G  = '\033[32m' # green

# create an instance of PyNet-class and run some functions
print(G+ PyNetTools.PyNet.__doc__ +W)
do = PyNetTools.PyNet()
do.dig('sbb.ch')
do.tping('sbb.ch', 443, 100) 
````

## Conclusion

The code for a Python module exists in a different file. There are a few different ways to import functions and values from modules and it’s easy to mess up.

When you work with modules, make sure that you reference the functions, classes, and variables that you want to access correctly.

You need to specify the exact function that you want to call from a module if you want to reference a function, rather than calling the module itself.
