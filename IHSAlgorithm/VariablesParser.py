# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:24:13 2020

@author: Adrian Czupak
"""


from math import *


#to żeby odczytywało funkcje zapisywane na rozne sposoby
def root(a, b): return pow(a, 1/b)
def ctan(x): return 1/tan(x)
def ctg(x): return ctan(x)
def tg(x): return tan(x)
def ln(x): return log(x)

class VariablesParser:
    def __init__(self, string, constants={}):
        self.__string = string
        self.__index = 0
        self.__constants = {
            'pi' : 3.141592653589793,
            'e' : 2.718281828459045 }
        self.__variables = []
        for var in constants.keys():
            if self.__constants.get(var) != None:
                raise Exception("Zmienna " + var + " jest juz zdefiniowana.")
            self.__constants[var] = constants[var]
        self.__deleteWhitespaces()
    
    
    #throws exceptions if wrong expression
    def getVariables(self):
        print()
        print(self.__string)
        print('where const:')
        print(self.__constants)
        self.__parse()
        if self.__hasNext():
            raise Exception("Unexpected character found: '" + self.__wrongExp + "'")
        return self.__variables
    
    
    def __deleteWhitespaces(self):
        string = ""
        for i in range(0, len(self.__string)):
            if self.__string[i] not in " \n\t\r":
                string += self.__string[i]
        self.__string = string 


    def __parse(self):
        return self.__parseAddition()
    
    
    def __parseAddition(self):
        self.__parseMultiplication()
        while True:
            char = self.__currentChar(1)
            if char == '+' or char == '-':
                self.__index += 1
                self.__parseMultiplication()
            else:
                break
    
    
    def __parseMultiplication(self):
        self.__parsePowering()
        while True:
            char = self.__currentChar(1)
            if char == '*' or char == '/':
                self.__index += 1
                self.__parsePowering()
            else:
                break
            
        
    def __parsePowering(self):
        self.__parseFunctions()
        char = self.__currentChar(1)
        if char == '^':
            self.__index += 1
            self.__parsePowering()
        else:
            pass
    
    
    def __parseFunctions(self):
        char = 0
        char2 = self.__currentChar(2)
        char3 = self.__currentChar(3)
        char4 = self.__currentChar(4)
        
        numOfArgs = 1
        if len(char2) == 2 and char2 in 'tg ln':
            char = char2
            self.__index += 2
        elif len(char3) == 3 and char3 in 'sin cos tan ctg log pow':
            char = char3
            self.__index += 3
            if char in 'log pow':
                numOfArgs = 2
        elif len(char4) == 4 and char4 in 'ctan root':
            char = char4
            self.__index += 4
            if char == 'root':
                numOfArgs = 2
        # Tu można dorzucić arctan itp
        
        if char != 0:
            if not self.__parseBrackets(numOfArgs):
                raise Exception("function should have brackets")
        else:
            self.__parseBrackets(1)
        
    def __parseBrackets(self, numOfArgs):
        char = self.__currentChar(1)
        if char == '(':
            self.__index += 1
            for i in range(numOfArgs):
                self.__parseAddition()
                if i < numOfArgs - 1:
                    if self.__currentChar(1) != ',':
                        raise Exception("To few arguments")
                    self.__index += 1
            if self.__currentChar(1) != ')':
                raise Exception("No closing bracket found")
            self.__index += 1
            return True
        else:
            self.__parseNegative()
            return False
    
    def __parseNegative(self):
        char = self.__currentChar(1)
        if char == '-':
            self.__index += 1
            self.__parseBrackets(1)
        else:
            self.__parseValue()
            
    def __parseValue(self):
        char = self.__currentChar(1)
        if char in '1234567890.':
            self.__parseNumber()
        else:
            self.__parseVariable()
        
        
    def __parseNumber(self):
        value = ''
        decimal_found = False
        char = ''
        
        while self.__hasNext():
            char = self.__currentChar(1)
            if char in '1234567890':
                value += char
            elif char == '.':
                if decimal_found:
                    raise Exception("Extra period")
                decimal_found = True
                value += '.'
            else:
                break
            self.__index += 1
        
        if len(value) == 0:
            if char == '':
                raise Exception("Unexpected end found")
            else:
                #to jest raczej wykluczone przez __parseValue() ...
                raise Exception("There should be a number")


    def __parseVariable(self):
        var = ''
        while self.__hasNext():
            char = self.__currentChar(1)
            if char.lower() in '_abcdefghijklmnopqrstuvwxyz0123456789':
                var += char
                self.__index += 1
            else:
                break
        
        value = self.__constants.get(var, None)
        if value == None and var not in self.__variables:  
            self.__variables.append(var)
            self.__wrongExp = var
            
        
    def __currentChar(self, charsNo):
        return self.__string[self.__index: self.__index + charsNo]
    
    def __hasNext(self):
        return self.__index < len(self.__string)
    
    
#ta funkcja do dopasowania do programu
def evaluate(expression, constants={}):
    try:
        p = VariablesParser(expression, constants)
        variables = p.getVariables()
        outStr = ''
        for var in variables:
            outStr += var
            if var != variables[len(variables) - 1]:
                outStr += ', '
        if outStr != '': return 'Variables: ' + outStr
        else: return 'No Variables'
    except Exception as ex:
        return ex.args   
