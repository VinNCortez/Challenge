# Configurando e iniciando os projetos
### Projeto Backend
Será necessário o python na versão 3.9 e o módulo pipenv instalado e adicionado ao path do sistema.

python 3.9: https://www.python.org/downloads/release/python-390/

pipenv: https://pipenv.pypa.io/en/latest/

Com o pipenv no path, rode o seguinte comando no terminal dentro do diretório '/backend':
```
pipenv install
```
Aguarde até que todas dependências sejam instaladas e o ambiente virtual seja criado

Depois de finalizado, será necessário entrar no ambiente virtual do python com as dependências do projeto.
Para isso basta rodar o comando:

```
pipenv shell
```

Agora o servidor já pode ser iniciado com o comando:
```
uvicorn main:app --port 80
```
No exemplo foi informada a porta 80, você pode utilizar outras, no entanto será necessário
informar nas configurações do frontend qual a url e porta do projeto backend (api)


### Projeto Frontend
Será necessário NodeJS e o NPM.

https://nodejs.org/en/download/

Com o NodeJS já instalado, digite o seguinte comando dentro do terminal e 
no diretório frontend: 
```
npm install
```
Depois de finalizado você deverá no arquivo /frontend/.env alterar a variável
VUE_APP_API_URL para a url correta do projeto backend caso necessário.

Por fim basta iniciar o servidor com o comando:
```
npm run serve
```
