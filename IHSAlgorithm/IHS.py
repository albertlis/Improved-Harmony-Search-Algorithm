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

'''

import copy
from VariablesParser import *
from random import uniform 


class IHSAlgorithm:
    def __init__(self):
        self.__HM = []          #Harmony Memory
        self.__HMS = 4          #Harmony Memory Size
        self.__HMCRmax = 0.9    #Harmony Memory Considering Rate
        self.__HMCRmin = 0.1
        self.__PARmax = 1       #Pitch Adjusting Rate
        self.__PARmin = 0.1
        self.__BWmax = 1        #Band Width
        self.__BWmin = 0.1
        self.__Tmax = 10        #Max Iteration Times
        self.__upperBound = 10000
        self.__lowerBound = -10000
        self.__variables = ['x1', 'x2', 'x3']
        self.__isContinuous = True
        self.__generation = 0
        
    
    def initializeHM(self):
        for var in self.__variables:
            for i in range(self.__HMS):
                self.__HM[var].append( uniform(self.__lowerBound, self.__upperBound))
                
                
    def generateNewVectors(self):       
        for x in range(len(self.__HM)):
            self.__HM[x] = self.__considerateMemory(self.__HM[x])
            self.__HM[x] = self.__adjustPitch(self.__HM[x])
            
        
    def __considerateMemory(self, newX):
        for i in range(len(newX)):
            if uniform(0, 1) >= self.__getHMCR(): #gdzies trzeba dac dziedzine X
                newX[i] = uniform(self.__lowerBound, self.__upperBound)
        return newX
                
                
    def __adjustPitch(self, newX):
        for i in range(len(newX)):
            random = uniform(-1, 1)
            if abs(random) < self.__getPAR():
                if self.__isContinuous:
                    newX[i] = newX[i] + random * self.__getBW()
                else:
                    pass #to w sumie nie bedzie uzywane
            else:
                pass #tu co ma byc ????????????????????????????????????????
        return newX
          
     
    def __getHMCR(self):
        return (self.__HMCRmax - self.__generation * 
                (self.__HMCRmax - self.__HMCRmin) / self.__Tmax)
        
        
    def __getPAR(self):
        return (((self.__PARmax - self.__PARmin) / (pi / 2)) *
                atan(self.__generation) + self.__PARmin)
        
        
    def __getBW(self):
        return (self.__BWmax - self.__generation * 
                (self.__BWmax - self.__BWmin) / self.__Tmax)