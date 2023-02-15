**Português (BR)** | [English (US)](/docs/TROUBLESHOOTING-en-US.md)
    
# Solução de Problemas

## `Python.h` faltando

Ao rodar o comando `pip install`, você pode obter o seguinte erro:

```
module.c:1:10: fatal error: Python.h: No such file or directory
     #include <Python.h>
              ^~~~~~~~~~
    compilation terminated.
    error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```
Tente instalar `python3-dev`. Por exemplo, via `apt install python3-dev`, se você está usando uma distro Debian, ou utilize o gerenciamento de pacotes da sua distro (por exemplo, `python3.6-dev` or `python3.7-dev`). Você pode saber qual é a sua versão via `python3 --version`.