# Chat de Voz Bot 🗣

[![Donate](https://img.shields.io/static/v1?label=Assine&message=PicPay&color=green)](https://grf.xyz/assine)
[![Donate](https://img.shields.io/static/v1?label=Colabore&message=PicPay&color=brightgreen)](https://grf.xyz/picpay)
[![Twitter Follow](https://img.shields.io/twitter/follow/espadrine.svg?style=social&label=Follow)](https://twitter.com/gabrf)

* [Sobre](#sobre)
* [Instruções de Uso](#instruções-de-uso)

## Sobre

Este bot tem a função de receber mensagens de voz de usuários para que sejam inseridas em chats de voz ou qualquer outro meio desejado.

## Configurar Projeto

Após clonar/baixar o repositório, instale os pacotes necessários:

`` `
pip install -r requisitos.txt
`` `

Crie um arquivo `chatdevozbot.conf` seguindo` chatdevozbot.conf_sample`.

Use o campo `TOKEN` para adicionar sua token de bot gerado por [@BotFather](https://t.me/BotFather)

Use o campo `CHATDEVOZ_LOG` para adiconar seu arquivos de log

Crie as estrutura de tabelas para o banco de dados
```
CREATE TABLE ChatDeVoz (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        groupid TEXT,
        adminid TEXT,
        pinid TEXT);

CREATE TABLE Chats_de_Voz (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        groupid TEXT,
        messageid TEXT);
```
## Executando Projeto

Para executar o projeto, faça: 

` `` 
python bot.py 
`` `

## Instruções de Uso

Adicione o bot como administrador em seu grupo.

Envie o comando `/iniciar` no grupo.

A partir deste momento o bot será capaz de receber as mensagens de voz e as encaminhará para quem enviou o comando `/iniciar`.

Para parar, envie no grupo `/parar`.

## Contribuição

São bem-vindos problemas via pull request! 
