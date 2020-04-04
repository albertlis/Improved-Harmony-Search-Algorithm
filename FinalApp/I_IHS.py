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

Dodać obsługę wszystkich granic dla pojedyńczych zmiennych

'''
"""
        Error list
-prawdopodobnie getter nie dziala po modyfikacji setPair
"""
from IHS import *


class I_IHSAlgorithm(IHSAlgorithm):
    # dodac nowe okno z bw
    def __init__(self, parameters, BW=[0.2, 0.8]):
        IHSAlgorithm.__init__(self)
        assert len(parameters) == 7
        self.setHMCR(list(parameters[3:5]))
        self.setPAR(parameters[5:7])
        self.setBW(BW)
        self.setHMS(parameters[2])
        self.setTmax(parameters[1])
        self.setVariables(parameters[0])
        self._setDefaultBounds()
        self.setFunction(parameters[0])
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
        assert len(inputList) == 2, parameter + " input list has wrong size"
        assert isinstance(inputList[0], float) and isinstance(inputList[1], float), parameter + \
                                                                                    " should be a pair of floats"
        try:
            parameterMin = float(inputList[0])
            parameterMax = float(inputList[1])
        except ValueError:
            raise ValueError(parameter + " its floats but something went wrong")

        assert parameterMin <= parameterMax, parameter + ": parameterMin should be <= parameterMax"
        assert parameterMin >= minLimit, parameter + ": parameterMin should be >= minLimit"
        assert parameterMax <= maxLimit, parameter + ": parameterMax should be <= maxLimit"
        exec('self._' + parameter + 'max = parameterMax')
        exec('self._' + parameter + 'min = parameterMin')

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
                'lambda self, X: self._objective_function(%s)' % strOfVarsFinal
            )
        except SyntaxError:
            # messageBox
            print('Nieprawidłowa funkcja')
        except NameError as err:
            # messageBox
            print('Niezdefiniowana zmienna: "' + str(err.args) + '"')
        except Exception as err:
            # messageBox
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


# aktualnie nie dziala
"""if __name__ == "__main__":
    def initIHS(HMS, HMCR, PAR, BW, Tmax, function):
        # HMCR = [min, max] ...
        ihs = I_IHSAlgorithm(HMS, HMCR, PAR, BW, Tmax, function)
        ihs.doYourTask()
        # dodac funkcje zwracania wynikow.

        return ihs"


    Tmax = 2000

    ihs = initIHS(10, [0.2, 0.8], [0.2, 0.8], [0.2, 0.8], Tmax,
                  "2 * pow(x1, 2) + pow(x2 - 3, 2) + 5")

    print(ihs._f)
    print(ihs._HM)"""
