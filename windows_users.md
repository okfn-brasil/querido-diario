# Windows 7+ users setup

If you're using Windows 7+ / Windows Server 2003+, setting up the project in the beginning gets a bit more tricky. But don't worry, this will be only in the beginning and we're here to guide you.

It is recommended to use Chocolatey to help you to install the required programs. Chocolatey is a software management solution similar to brew in Mac/Linux that installs programs with a simple command. You can download it using their instructions: https://chocolatey.org/docs/installation. After installation, you might need to restart your PowerShell window or Prompt commands (cmd). 

If you don't have the below programs already, you can download them using the line code in PowerShell or Prompt commands (cmd):
- Docker Toolbox: `choco install docker-toolbox`
- Make: `choco install make`
- Python3: `choco install python3`
- Git: `choco install git`

After the installation, you should restart the PowerShell window or Prompt commands (cmd) before you go to the next step.

You need to run `Docker Quickstart Terminal` so the virtual machine is created for the first time. After you see the whale there, you’ll be able to run `make setup`. So that's it! Now you need to go back to [README.md](README.md) and follow the instructions from there. 

**Note**
If you use PowerShell to download Chocolatey, you will need PowerShell version 3+. To check your version, open PowerShell with a right-click and run as administrator. Then run `Get-Host | Select-Object Version`, this will give you the current version you're using. If you don't have version 3+, you can update it at https://www.microsoft.com/en-us/download/details.aspx?id=34595


---------------------------------------------
# Configuração para usuários de Windows 7+

Se você está usando Windows 7+ / Windows Server 2003+, configurar o projeto no início pode ser um pouco mais complicado. Mas não se preocupe, só é necessário fazer isso no começo e estamos aqui para te guiar.

É recomendado usar Chocolatey para te ajudar a instalar os programas necessários. Chocolatey é um programa para administrar soluções que instala programas com um simples comando, é similar ao brew do Mac/Linux. Você pode baixar usando as instruções em: https://chocolatey.org/docs/installation. Após a instalação do Choco, você deve reiniciar seu PowerShell ou Prompt de comando (cmd). 

Se você ainda não tem algum dos programas abaixo, deve baixar utilizando essa linha de comando no PowerShell ou Prompt de comando (cmd):
- Docker Toolbox: `choco install docker-toolbox`
- Make: `choco install make`
- Python3: `choco install python3`
- Git: `choco install git`

Após a instalação dessas ferramentas, você deve reiniciar  seu PowerShell ou Prompt de comando (cmd) para seguir os próximos passos..

Agora, você precisa abrir `Docker Quickstart Terminal` para que a máquina virtual seja criada pela primeira vez. E pronto! Seu computador tem todas as ferramentas necessárias para você começar a contribuir com o Querido Diário.

Vai lá no arquivo [README.md](README.md) e segue as instruções  para rodar o `make setup`.

**Nota:**
Se você for usar PowerShell para baixar Chocolatey, deverá utilizar a versão 3+. Para verificar sua versão do PowerShell, abra-o como administrador e rode `Get-Host | Select-Object Version`, isso te mostrará qual sua versão. Se não for a versão 3+, você pode atualizá-la seguindo as instruções no site https://www.microsoft.com/en-us/download/details.aspx?id=34595