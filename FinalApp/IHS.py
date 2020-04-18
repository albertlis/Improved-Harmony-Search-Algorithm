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
        self._f = np.empty(self._HMS)
        self._isContinuous = True
        self._generation = 0
        self._objective_function = lambda X: sum(X)
        self.compute = lambda X: self._objective_function(X)
        self._trace = []

    def initializeHM(self):
        self._f = np.empty(self._HMS)
        for i in range(self._HMS):
            X = {}
            for var in range(len(self._variables)):
                X.update({self._variables[var]:
                              uniform(self._varLowerBounds[var],
                                      self._varUpperBounds[var]
                                      )
                          })
            self._HM.append(X)
            self._f[i] = self.compute(self, X)

    def improvise(self):
        new = {}
        for i, variables in enumerate(self._variables):
            upperBound = self._varUpperBounds[i]
            lowerBound = self._varLowerBounds[i]
            # memoryConsideration
            if uniform(0, 1) < self._HMCR:
                D1 = int(uniform(0, self._HMS))
                D2 = self._HM[D1].get(variables)
                new.update({variables: D2})

                # pitchAdjustment
                if uniform(0, 1) < self._PAR:
                    if uniform(0, 1) < 0.5:
                        D3 = (new.get(variables) -
                              uniform(0, self._BW)
                              )
                        if lowerBound <= D3:
                            new.update({variables: D3})
                    else:
                        D3 = (new.get(variables) +
                              uniform(0, self._BW)
                              )
                        if upperBound >= D3:
                            new.update({variables: D3})

            else:
                new.update({variables: uniform(lowerBound,
                                                upperBound )})

        return new

    def updateHM(self, new):
        f = self.compute(self, new)
        # for finding minimum
        fMaxValue = np.amax(self._f)
        if f < fMaxValue:
            for i, value in enumerate(self._f):
                if fMaxValue == value:
                    self._f[i] = f
                    self._HM[i] = new
                    break

    def _findTrace(self):
        index = np.argmin(self._f)
        variables = self._HM[index]
        if variables not in self._trace:
            self._trace.append(variables)

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
            self._findTrace()

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
        index = np.argmin(self._f)
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

    def getTrace(self):
        return self._trace
