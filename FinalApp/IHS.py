# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:10:54 2020

@author: Adrian Czupak
"""

'''

    IHSAlgorithm to klasa obsługująca całą logikę algorytmu z założeniem,
że zostały do niej wprowadzone dobre dane (zapewnia to Child Class
I_IHSAlgorithm)

    Własciwosci IHSAlgorithm sa settowane przez I_IHSAlgorithm, która wyklucza
błędy wprowadzania w GUI. Tutaj należy jeszcze ogarnąć, czy przypisywanie
self.<element ParentClass> rzeczywiscie przypisuje do ParentClass, bo
raczej trzeba będzie to robić przez ParentClass.<element ParentClass>...
    
    Na bieżąco dopisywane funkcje...

Do optymalizacji:
- w updateHM() linia if max(self._f) == self._f[i]: generuje duży narzut obliczeniowy
lepiej max sprawdzić raz zamiast w każdej iteracji. Promlem będzie się objawiał przy dużym HM

'''

import copy
from random import uniform
from VariablesParser import *


class IHSAlgorithm:
    def __init__(self):
        self._HM = []  # Harmony Memory
        self._HMS = 4  # Harmony Memory Size
        self._HMCRmax = 0.9  # Harmony Memory Considering Rate
        self._HMCRmin = 0.1
        self._PARmax = 1  # Pitch Adjusting Rate
        self._PARmin = 0.1
        self._BWmax = 10  # Band Width
        self._BWmin = 0
        self._Tmax = 10  # Max Iteration Times
        self._variables = []
        self._varUpperBounds = []
        self._varLowerBounds = []
        self._f = []
        self._isContinuous = True
        self._generation = 0
        self._objective_function = lambda X: sum(X)
        self.compute = lambda X: self._objective_function(X)

    def initializeHM(self):
        self._HM = []
        for i in range(self._HMS):
            X = {}
            for var in range(len(self._variables)):
                X.update({self._variables[var]:
                              uniform(self._varLowerBounds[var],
                                      self._varUpperBounds[var]
                                      )
                          })
            self._HM.append(X)
            self._f.append(self.compute(self, X))

    def dodo(self):
        exec(
            'self._objective_function = lambda ' + 'x' + ': ' + 'x + 1'
        )
        exec(
            "self.compute = lambda self, X: self._HMS + X['x']"
        )
        ddd = {'x': 1.5}
        self._f.append(self.compute(self, ddd))

    def improvise(self, curr):
        new = {}
        for i in range(len(self._variables)):
            if uniform(0, 1) < self._getHMCR():
                D1 = int(uniform(0, 1) * self._HMS)
                D2 = self._HM[D1].get(self._variables[i])
                new.update({self._variables[i]: D2})

                if uniform(0, 1) < self._getPAR():
                    if uniform(0, 1) < 0.5:
                        D3 = (new.get(self._variables[i]) -
                              uniform(0, 1) * self._getBW()
                              )
                        if self._varLowerBounds[i] <= D3:
                            new.update({self._variables[i]: D3})
                    else:
                        D3 = (new.get(self._variables[i]) +
                              uniform(0, 1) * self._getBW()
                              )
                        if self._varUpperBounds[i] >= D3:
                            new.update({self._variables[i]: D3})

            else:
                new.update({self._variables[i]:
                                uniform(self._varLowerBounds[i],
                                        self._varUpperBounds[i]
                                        )})

        return new

    def updateHM(self, curr, new):
        f = self.compute(self, new)
        # for finding minimum
        if f < max(self._f):
            for i in range(len(self._f)):
                if max(self._f) == self._f[i]:
                    self._f[i] = f
                    self._HM[i] = new

    def doYourTask(self):
        while self._generation < self._Tmax:
            self._generation += 1
            new = self.improvise((self._generation - 1) % self._HMS)
            self.updateHM((self._generation - 1) % self._HMS, new)

    def _getHMCR(self):
        return (self._HMCRmax - self._generation *
                (self._HMCRmax - self._HMCRmin) / self._Tmax)

    def _getPAR(self):
        return (self._PARmin + self._generation *
                (self._PARmax - self._PARmin) / len(self._variables))

    def _getBW(self):
        c = log(self._BWmin / self._BWmax)
        return self._BWmax * exp(self._generation * c)

    def getVariables(self):
        return self._variables
