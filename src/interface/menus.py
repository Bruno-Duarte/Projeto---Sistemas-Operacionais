import sys

LINE_LENGTH = 60


def draw_line():
	print(LINE_LENGTH*'=')

def main_menu():
	draw_line()
	print('1. Imprimir')
	print('2. Sair')
	print()

def secondary_menu():
	draw_line()
	print('Escolha um dos seguintes algoritmos para a impressora: ')
	print()
	print('1. Dekker')
	print('2. Peterson')
	print('3. Lamport')
	print()
	option = input('Ou digite 4 (quatro) para sair: ')
	return option
