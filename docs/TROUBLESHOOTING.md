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

## Erro `pinned with ==`

Ao realizar o pip install requeriments pode ocorrer um erro de fixação inexata, então utilize o "--no-deps" ao instalar:

~~~Linux
pip install -r data_collection/requirements-dev.txt --no-deps
~~~

##  Erro `legacy-install`

Ao instalar bibliotecas pode ocorrer o seguinte erro no seu terminal WSL:

```
error: legacy-install failure
error: command 'x86_64-linux-gnu-gcc' failed: No such file or directory
```

Então faça o upgrade do pip e instale algumas bibliotecas essenciais do Linux:

~~~Linux
python3 -m pip install --upgrade pip
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
~~~
