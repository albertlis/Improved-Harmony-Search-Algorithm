# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:10:54 2020

@author:
    Adrian Czupak & Albert Lis
"""
from pprint import pprint

import numpy as np

'''

    IHSAlgorithm to klasa obsługująca całą logikę algorytmu z założeniem,
że zostały do niej wprowadzone dobre dane (zapewnia to Child Class
I_IHSAlgorithm)

updateHM() - przyjmuje parametr curr który jest nieużywany


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
        self._BWmin = 0.0001
        self._Tmax = 1000  # Max Iteration Times
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

    def improvise(self):
        new = {}
        for i in range(len(self._variables)):

            # memoryConsideration
            if uniform(0, 1) < self._HMCR:
                D1 = int(uniform(0, 1) * self._HMS)
                D2 = self._HM[D1].get(self._variables[i])
                new.update({self._variables[i]: D2})

                # pitchAdjustment
                if uniform(0, 1) < self._PAR:
                    if uniform(0, 1) < 0.5:
                        D3 = (new.get(self._variables[i]) -
                              uniform(0, 1) * self._BW
                              )
                        if self._varLowerBounds[i] <= D3:
                            new.update({self._variables[i]: D3})
                    else:
                        D3 = (new.get(self._variables[i]) +
                              uniform(0, 1) * self._BW
                              )
                        if self._varUpperBounds[i] >= D3:
                            new.update({self._variables[i]: D3})

            else:
                new.update({self._variables[i]:
                                uniform(self._varLowerBounds[i],
                                        self._varUpperBounds[i]
                                        )})

        return new

    def updateHM(self, new):
        f = self.compute(self, new)
        # for finding minimum
        fMaxValue = max(self._f)
        if f < fMaxValue:
            for i in range(len(self._f)):
                if fMaxValue == self._f[i]:
                    self._f[i] = f
                    self._HM[i] = new
                    break

        # for finding maximum
        '''
        fMaxValue = min(self._f)
        if f < fMaxValue:
            for i in range(len(self._f)):
                if fMaxValue == self._f[i]:
                    self._f[i] = f
                    self._HM[i] = new
                    break
                    '''

    def doYourTask(self):
        self.initializeHM()
        while self._generation < self._Tmax:
            self._generation += 1
            self._updateHMCR()
            self._updatePAR()
            self._updateBW()
            new = self.improvise()  # (self._generation - 1) % self._HMS
            self.updateHM(new)

    def _updateHMCR(self):
        self._HMCR = (self._HMCRmax - self._generation *
                      (self._HMCRmax - self._HMCRmin) / self._Tmax)

    def _updatePAR(self):
        self._PAR = (self._PARmin + self._generation *
                     (self._PARmax - self._PARmin) / len(self._variables))

    def _updateBW(self):
        c = log(self._BWmin / self._BWmax)
        self._BW = self._BWmax * exp(self._generation * c)

    def getOptimalSolution(self):
        f = np.array(self._f)
        index = int(np.argmin(f))
        functionValue = self._f[index]
        variables = self._HM[index]
        preparedVariables = []
        for key, value in variables.items():
            try:
                preparedVariables.append(f'{key}:\t{value}')
            except TypeError as e:
                print(e)
                return
        return functionValue, preparedVariables
