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


from IHS import IHSAlgorithm

class I_IHSAlgorithm(IHSAlgorithm):
    def __init__(self):
        IHSAlgorithm.__init__(self)
    
    # W setterach poustawiać granice w jakich mogą się znaleźć dane parametry
    def setHMS(self, HMS):
        if HMS >= 0:
            self.__HMS = HMS
        else:
            raise Exception("HMS should be bigger than 0")
            
            
    def setHMCR(self, minimum, maximum): #tu jeszcze pytanie o granice 
        HMCRmin = 0
        HMCRmax = 1
        if minimum >= HMCRmin and maximum <= HMCRmax and minimum <= maximum:
            self.__HMCRmax = maximum
            self.__HMCRmin = minimum
        else:
            if(minimum <= maximum):
                raise Exception("PAR should be in [" + str(HMCRmin) + "; "
                                + str(HMCRmax) + "] range")
            else:
                raise Exception("'min' should be less than 'max'")
                
                
    def setBW(self, minimum, maximum): #tu jeszcze pytanie o granice 
        BWmin = 0
        BWmax = 1
        if minimum >= BWmin and maximum <= BWmax and minimum <= maximum:
            self.__BWmax = maximum
            self.__BWmin = minimum
        else:
            if(minimum <= maximum):
                raise Exception("PAR should be in [" + str(BWmin) + "; "
                                + str(BWmax) + "] range")
            else:
                raise Exception("'min' should be less than 'max'")
            
    
    def setPAR(self, minimum, maximum): #tu jeszcze pytanie o granice 
        PARmin = 0
        PARmax = 1
        if minimum >= PARmin and maximum <= PARmax and minimum <= maximum:
            self.__PARmax = maximum
            self.__PARmin = minimum
        else:
            if(minimum <= maximum):
                raise Exception("PAR should be in [" + str(PARmin) + "; "
                                + str(PARmax) + "] range")
            else:
                raise Exception("'min' should be less than 'max'")
    
    
    def setTmax(self, Tmax):
        try:
            Tmax = int(Tmax)
        except:
            raise Exception("Tmax should be an integer")
        
        if Tmax <= 1:
            raise Exception("Tmax should be bigger than 1")
        else:
            self.__Tmax = Tmax
    
    
    def setVariables(self, variables):
        for var in variables:
            if str(var)[0] not in 'qwertyuiopasdfghjklzxcvbnm':
                raise Exception("Wrong name of variable")
            else:
                self.__variables.append(var)
      
        
    def setFunction(self, string): 
        strOfVars = ''
        strOfVarsFinal = ''
        for var in self.__variables:
            strOfVars += var
            strOfVarsFinal += "X[" + var + "]"
            if var != self.__variables[-1]:
                strOfVars += ', '
                strOfVarsFinal += ', '
        try:
            IHSAlgorithm.__objective_function = eval('lambda '
                + strOfVars + ': ' + string)
            IHSAlgorithm.compute = eval('lambda X: '
                + 'self.__objective_function(%s)'%strOfVarsFinal)
        except SyntaxError:
            # messageBox
            print('Nieprawidłowa funkcja')
        except NameError as err:
            #messageBox
            print('Niezdefiniowana zmienna: "' + err.args + '"')
        else:
            #messageBox
            print("Nieznany błąd")
    