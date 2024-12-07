# Flow.Launcher.Plugin.PyRepl
A python repl implimentation in flow

## Features
### Returning results without printing

The first result that PyRepl will return is the result of the input.

![](assets/py_100_result.png)

### Accessing previous result

Before PyRepl returns the result, it will set the previous result to the `_` variable, so to access the previous result, use `_`.

![Example](assets/py__times_10_result.png)

### Viewing the console in flow

After the input's result, PyRepl will show each line that was printed to the console as a result.

![Example](assets/console_example.png)

### Viewing full tracebacks

In the case of an error, PyRepl will create a window that contains the traceback to easily access and read it.

![Example](assets/traceback_example.png)