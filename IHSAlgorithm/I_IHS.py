# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:27:20 2020

@author: Adrian Czupak
"""


'''

    Klasa I_IHSAlgorithm czysci wejscie z GUI i wprowadza do IHSAlgorithm

    Trzeba jeszcze ogarnąć, czy na pewno wpisałem dobre granice dla parametrów
w setterach
    
    W setterach sprawdzać, czy dobry typ danych wprowadzony (czy nie stringi)

    Teraz jeszcze próbuję ogarnąć jak zapisać HarmonyMemory (__HM), żeby można
było jakos logicznie je iterować (I mean sth. like self.__variables['x1'][1])
(patrz: implementacja I_IHSAlgorithm.setFunction() -> przekazywanie argumentów
do wyrażenia lambda)

'''


from IHS import *


class I_IHSAlgorithm(IHSAlgorithm):
    def __init__(self, HMS, HMCR, PAR, BW, Tmax, function):
        IHSAlgorithm.__init__(self)
        self.setHMCR(HMCR)
        self.setPAR(PAR)
        self.setBW(BW)
        self.setHMS(HMS)
        self.setTmax(Tmax)
        self.setVariables(function)
        self._setDefaultBounds()
        self.setFunction(function)
        self.initializeHM()
    
    # W setterach poustawiać granice w jakich mogą się znaleźć dane parametry
    def setHMCR(self, HMCR):
        self._setPair('HMCR', 0, 1, HMCR)
        
    def setPAR(self, PAR):
        self._setPair('PAR', 0, 1, PAR)
        
    def setBW(self, BW):
        self._setPair('BW', -100, 100, BW)
        
    def setTmax(self, Tmax):
        self._setInteger('Tmax', Tmax)
    
    def setHMS(self, HMS):
        self._setInteger('HMS', HMS)
        
    def _setPair(self, parameter, minLimit, maxLimit, inputList):
        if type(inputList) == list and len(inputList) == 2:
            try:
                inputList[0] = float(inputList[0])
                inputList[1] = float(inputList[1])
            except:
                raise Exception(parameter + " should be a pair of floats")
            minimum = min(inputList)
            maximum = max(inputList)      
        else:
            raise Exception("There should be min and max of " + parameter)
            
        if minimum >= minLimit and maximum <= maxLimit:
            exec('self._' + parameter + 'max = maximum')
            exec('self._' + parameter + 'min = minimum')
        else:
            raise Exception(parameter + "should be in [" + str(minLimit) + "; "
                            + str(maxLimit) + "] range")
    
    
    def _setInteger(self, parameter, value):
        try:
            value = int(value)
        except:
            raise Exception(parameter + " should be an integer")
        
        if value <= 1:
            raise Exception(parameter + " should be bigger than 1")
        else:
            exec('self._' + parameter + ' = value')
            
    
    def setVariables(self, expression, constants={}):
        try:
            p = VariablesParser(expression, constants)
            variables = p.getVariables()
            self._variables = variables
        except Exception as ex:
            # messageBox
            print(ex.args)  
            
            
    def setFunction(self, string):
        strOfVars = ''
        strOfVarsFinal = ''
        for var in self._variables:
            strOfVars += var
            strOfVarsFinal += "X['" + var + "']"
            if var != self._variables[-1]:
                strOfVars += ', '
                strOfVarsFinal += ', '
        try:
            self._objective_function = eval('lambda '
                + strOfVars + ': ' + string)
            self.compute = eval(
                'lambda self, X: self._objective_function(%s)'%strOfVarsFinal
                )
        except SyntaxError:
            # messageBox
            print('Nieprawidłowa funkcja')
        except NameError as err:
            #messageBox
            print('Niezdefiniowana zmienna: "' + err.args + '"')
        except Exception as err:
            #messageBox
            print(err.args)
            raise
            
            
    def setBounds(self, index, lower, upper):
        if len(self._varLowerBounds) <= index:
            self._varLowerBounds.append(lower)
            self._varUpperBounds.append(upper)
        else:
            self._varLowerBounds[index] = lower
            self._varUpperBounds[index] = upper
     
    
    def _setDefaultBounds(self):
        for i in range(len(self._variables)):
            self.setBounds(i, -10, 10)
 

def initIHS(HMS, HMCR, PAR, BW, Tmax, function):
    #HMCR = [min, max] ...
    ihs = I_IHSAlgorithm(HMS, HMCR, PAR, BW, Tmax, function)
    ihs.doYourTask()
    #dodac funkcje zwracania wynikow.
    
    return ihs

Tmax = 2000

ihs = initIHS(10, [0.2, 0.8], [0.2, 0.8], [0.2, 0.8], Tmax, 
        "2 * pow(x1, 2) + pow(x2 - 3, 2) + 5")
    
print(ihs._f)
print(ihs._HM)