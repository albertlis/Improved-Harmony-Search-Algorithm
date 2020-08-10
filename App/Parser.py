# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:01:41 2020

@author: Adrian Czupak
"""


'''

To jest plik roboczy, także nie ma co przeglądać :)


'''




from math import *

class DivisionByZero(Exception):
    pass

class MyException(Exception):
    pass


class Parser:
    def __init__(self, string, variables={}):
        self.__string = string
        self.__index = 0
        self.__variables = {
            'pi' : 3.141592653589793,
            'e' : 2.718281828459045 }
        for var in variables.keys():
            if self.__variables.get(var) != None:
                raise MyException("Zmienna " + var + " jest juz zdefiniowana.")
            self.__variables[var] = variables[var]
        self.__deleteWhitespaces()
    
    def getValue(self):
        print(self.__string)
        value = self.__parse()
        if self.__hasNext():
            raise MyException("Unexpected character found")
        return value
    
    def __deleteWhitespaces(self):
        string = ""
        for i in range(0, len(self.__string)):
            if self.__string[i] not in " \n\t\r":
                string += self.__string[i]
        self.__string = string 

    def __parse(self):
        return self.__parseAddition()
    
    def __parseAddition(self):
        numbers = [self.__parseMultiplication()]
        while True:
            char = self.__currentChar(1)
            if char == '+':
                self.__index += 1
                numbers.append(self.__parseMultiplication())
            elif char == '-':
                self.__index += 1
                numbers.append(-1 * self.__parseMultiplication())
            else:
                break
        return sum(numbers)
    
    def __parseMultiplication(self):
        numbers = [self.__parsePowering()]
        while True:
            char = self.__currentChar(1)
            if char == '*':
                self.__index += 1
                numbers.append(self.__parsePowering())
            elif char == '/':
                self.__index += 1
                denominator = self.__parsePowering()
                if denominator == 0:
                    exceptString = ''
                    for var in self.__variables.keys():
                        exceptString += (var + " = " 
                                         + str(self.__variables[var]) + "; ")
                    raise DivisionByZero('Division by zero for variables: ' 
                                      + exceptString)
                numbers.append(1.0 / denominator)
            else:
                break
        value = 1.0
        for val in numbers:
            if val != None:
                value *= val
        return value
        
    def __parsePowering(self):
        base = self.__parseFunctions()
        char = self.__currentChar(1)
        if char == '^':
            self.__index += 1
            exponent = self.__parsePowering()
            return pow(base, exponent)
        else:
            return base
    
    def __parseFunctions(self):
        char = 0
        char2 = self.__currentChar(2)
        char3 = self.__currentChar(3)
        char4 = self.__currentChar(4)
                   
        if len(char2) == 2 and char2 in 'tg':
            char = char2
            self.__index += 2
        elif len(char3) == 3 and char3 in 'sin cos tan ctg log':
            char = char3
            self.__index += 3
        elif len(char4) == 4 and char4 in 'ctan':
            char = char4
            self.__index += 4
        # Tu można dorzucić arctan itp, tylko wtedy trzeba się bawic z dziedzina
            
        if char != 0:
            argument = self.__parseBrackets()
            if argument == None:
                raise MyException("'%s' function not filled"%char3)
            if char in 'tg tan':
                try:
                    return tan(argument)
                except:
                    raise DivisionByZero("Tangens = infinity")
            if char in 'sin':
                return sin(argument)
            if char in 'cos':
                return cos(argument)
            if char in 'ctg ctan':
                try:
                    return 1/tan(argument)
                except:
                    raise DivisionByZero("Cotangens = infinity")
            if char in 'log':
                if argument <= 0:
                    raise DivisionByZero("Logarithm argument negative")
                return log(argument)
        else:
            return self.__parseBrackets()
        
    def __parseBrackets(self):
        char = self.__currentChar(1)
        if char == '(':
            self.__index += 1
            value = self.__parseAddition()
            if self.__currentChar(1) != ')':
                raise MyException("No closing bracket found")
            self.__index += 1
            return value
        else:
            return self.__parseNegative()
    
    def __parseNegative(self):
        char = self.__currentChar(1)
        if char == '-':
            self.__index += 1
            return -1 * self.__parseBrackets()
        else:
            return self.__parseValue()
            
    def __parseValue(self):
        char = self.__currentChar(1)
        if char in '1234567890.,':
            return self.__parseNumber()
        else:
            return self.__parseVariable()
        
    def __parseNumber(self):
        value = ''
        decimal_found = False
        char = ''
        
        while self.__hasNext():
            char = self.__currentChar(1)
            if char in '1234567890':
                value += char
            elif char in '.,':
                if decimal_found:
                    raise MyException("Extra period")
                decimal_found = True
                value += '.'
            else:
                break
            self.__index += 1
        
        if len(value) == 0:
            if char == '':
                raise MyException("Unexpected end found")
            else:
                #to jest raczej wykluczone przez __parseValue() ...
                raise MyException("There should be a number")
        
        return float(value)
        
    def __parseVariable(self):
        var = ''
        while self.__hasNext():
            char = self.__currentChar(1)
            if char.lower() in '_abcdefghijklmnopqrstuvwxyz0123456789':
                var += char
                self.__index += 1
            else:
                break
        
        value = self.__variables.get(var, None)
        if value == None:
            
            raise MyException("Unrecognized variable '%s'"%var)
        return float(value)
        
    def __currentChar(self, charsNo):
        return self.__string[self.__index: self.__index + charsNo]
    
    def __hasNext(self):
        return self.__index < len(self.__string)

def evaluate(expression, variables={}):
    try:
        p = Parser(expression, variables)
        value = p.getValue()
    except MyException as ex:
        print(ex.args)
        raise
    except Exception as ex:
        print(ex.args)
        raise
    
    if int(value) == value:
        return int(value)

    epsilon = 0.00000001
    if int(value + epsilon) != int(value):
        return int(value + epsilon)
    elif int(value - epsilon) != int(value):
        return int(value)
    
    return value

print(evaluate("1 + 2 * 3"))
print(evaluate("(1 + 2) * 3"))
print(evaluate("-(1 + 2) * 3"))
print(evaluate("(1-2)/3.0 + 0.0000"))
print(evaluate("1 + pi / 4"))
print(evaluate("(a + b) / c", { 'a':1, 'b':2, 'c':3 }))
print(evaluate("(x + e * 10) / 10", { 'x' : 3 }))
print(evaluate("1.0 / 3 * 6"))
print(evaluate("(1 - 1 + -1) * pi"))
print(evaluate("pi * e"))
print(evaluate("sin(pi/3)^3+2/log(21*e)"))


'''
expression = "(a + b) / c"
variables222 = { 'a':1, 'b':2, 'c':3 }
try:
    p = Parser(expression, variables222)
    value = p.getValue()
except MyException as ex:
    print(ex.args)
    raise
except Exception as ex:
    print(ex.args)
    raise

if int(value) == value:
    print(int(value))

epsilon = 0.00000001
if int(value + epsilon) != int(value):
    print(int(value + epsilon))
elif int(value - epsilon) != int(value):
    print(int(value))
'''


#or just
x = [1, 2, 3]
print(eval("sin(pi/3)*3+2/log(21*e)"))