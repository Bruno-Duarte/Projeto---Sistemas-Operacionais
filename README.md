## Simulação de Espera Ocupada para a Disciplina de Sistemas Operacionais (UECE/2019) ##

Esse é o projeto final para a disciplina de Sistemas Operacionais do curso de Ciência da Computação 
da Universidade Estadual do Ceará (UECE), semestre 2019.1. O objetivo é apresentar um problema de 
exclusão mútua em um cenário realístico de SO e implementar soluções para o mesmo usando os Algoritmos 
de Dekker, Peterson e Lamport. O cenário escolhido foi o de uma impressora conectada em rede na qual 
foi considerado como região crítica o intervalo de tempo em que um dado documento está em processo de 
impressão.

## Features

- utiliza o conceito de comunicação entre processos
- trabalha o uso de threads
- promove o uso de POO
- utiliza padrão de projeto

## Começando

Para executar o programa, será necessário ter instalado em sua máquina:

`python >= 3.5`

## Desenvolvimento

Para fazer alterações no projeto:

```
cd "diretorio de sua preferência"
git clone https://github.com/Bruno-Duarte/Projeto-Sistemas-Operacionais.git
```

## Execução

```
1. cd Projeto-Sistemas-Operacionais
2. python3 servidor.py
3. python3 impressora.py
4. python3 cliente.py
```
