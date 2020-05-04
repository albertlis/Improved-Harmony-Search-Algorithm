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
        self._NumOfIterations = 1000  # Max Iteration Times
        self._variables = []
        self._varUpperBounds = []
        self._varLowerBounds = []
        self._f = np.empty(self._HMS)
        self._generation = 0
        self._objective_function = lambda X: sum(X)
        self.compute = lambda X: self._objective_function(X)
        self._trace = []
        self._lastBestSolutionIteration = 0
                
    def initializeHM(self):
        def catchZeroDivision(i):
            inputVector = {}
            for counter, var in enumerate(self._variables):
                inputVector.update({var: uniform(self._varLowerBounds[counter], self._varUpperBounds[counter])})
            self._HM.append(inputVector)
            try:
                self._f[i] = self.compute(self, inputVector)
            except ZeroDivisionError or RuntimeWarning:
                print("Nie wolno '/0' - Nununu")
                raise
                
        self._f = np.empty(self._HMS)
        for i in range(self._HMS):
            catchZeroDivision(i)
                

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
            self._lastBestSolutionIteration = self._generation

    def doYourTask(self):
        def catchZeroDivision():
            try:
                new = self.improvise()  # (self._generation - 1) % self._HMS
                self.updateHM(new)
            except ZeroDivisionError or RuntimeWarning:
                print('i caughed ZeroDiv in IHS.updateHM')
                catchZeroDivision()
                
        self.initializeHM()
        while self._generation < self._NumOfIterations:
            self._generation += 1
            self._updateHMCR()
            self._updatePAR()
            self._updateBW()
            catchZeroDivision()
            self._findTrace()

    def _updateHMCR(self):
        self._HMCR = (self._HMCRmax - self._generation *
                      (self._HMCRmax - self._HMCRmin) / self._NumOfIterations)

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

    def getLastBestSolutionIteration(self):
        return self._lastBestSolutionIteration
