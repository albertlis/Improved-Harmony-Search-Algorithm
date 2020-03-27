# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:05:41 2020

@author: Adrian Czupak
"""

from VariablesParser import *


'''

    Funkcje evaluate nalezy dopasowac do wymagan programu

    Moj pomysl jest taki, zeby zwracala tablice zmiennych, ktora
mozna nastepnie przekazac do klasy algorytmu I_IHSAlgorithm.

    Dodatkowo dodac funkcje (np. controlInput()), ktora bedzie uruchamiana po
wyjsciu z inputBoxa do wprowadzania funkcji i bedzie zwracala komunikat, czy
funkcja jest napisana odpowiednio, a jesli nie to wypisze co jest zle
odpowiadaja za to wyjatki poumieszczane w klasie VariablesParser.



    W klasie I_IHS jest funkcja setFunction tworząca wyrażenie lambda ze
stringa wprowadzonego w inputBoxie i na tym wyrażeniu program powinien już
szybko działać. Klasa VariablesParser nie powinna dopuscic do uruchomienia
algorytmu w razie zle wpisanej funkcji

'''
print(evaluate("1 + 2 * 3"))
print(evaluate("(1 + 2) * 3"))
print(evaluate("-(1 + x1) * x2"))
print(evaluate("(1-2)/3.0 + 0.0000"))
print(evaluate("1 + pi / 4"))
print(evaluate("(a + b) / x", { 'a':1, 'b':2, 'c':3 }))
print(evaluate("(x + e * 10) / y"))
print(evaluate("1.0 / 3 * 6"))
print(evaluate("(1 - 1 + -1) * pi"))
print(evaluate("pi * e"))
print(evaluate("sin(pi/3)^3+2/log(21*e, 10)"))
print(evaluate("s(pi)"))
print(evaluate("sin(pi^x1)"))
print(evaluate("sin(pow(pi, x1))"))