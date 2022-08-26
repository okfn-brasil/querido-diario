**English (US)** | [Português (BR)](/docs/TROUBLESHOOTING.md)

# Troubleshooting

## `Python.h` missing

While running `pip install` command, you can get an error like this one below:

```
module.c:1:10: fatal error: Python.h: No such file or directory
     #include <Python.h>
              ^~~~~~~~~~
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```

Please try to install `python3-dev`. E.g. via `apt install python3-dev`, if you are using a Debian-like distro, or use your distro manager package. Make sure that you use the correct version (e.g. `python3.6-dev` or `python3.7-dev`). You can check your version via `python3 --version`.