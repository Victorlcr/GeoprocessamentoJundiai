# Geoprocessamento espacial de áreas verdes em Jundiaí

### Requisitos

- Python 3.12.3
- venv

## Instalação

Execute todos os comandos abaixo em ordem

``` sudo apt update && sudo apt upgrade ```

#### Acesse o diretório cloando, crie o ambiente virtual e ative-o

``` python3 -m venv . ```

``` source ./bin/activate ```

Certifique que foi ativado. O nome do diretório deve aparecer entre parênteses antes do caminho no terminal.

#### Instale as dependências

Python

``` pip install -r requirements.txt ```

Servidor Frontend

``` curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash ```

``` export NVM_DIR="$HOME/.nvm" ```

``` [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" ```

``` nvm install node ```

``` nvm install 14 ```

``` npm install -g http-server ```

#### Para iniciar os servidores execute

Back-end

``` uvicorn backend.app.main:app --reload ```

Front-end

``` cd ./frontend && http-server -p 5500 ```