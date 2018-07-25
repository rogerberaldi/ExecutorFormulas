"""
Created on 21 de jul de 2018

@author: Ryan Gazaniga <ryangazaniga@gmail.com>
"""


class myFormula:
    def __init__(self):
        pass
    
    def __celsius_to_kelvin(self, c):
        c = float(c)
        result = c + 273
        return result

    def __kelvin_to_celsius(self, k):
        k = float(k)
        result = k - 273
        return result

    def __celsius_to_fahrenheit(self,c):
        c = float(c)
        result = 1.8 * c + 32
        return result

    def __fahrenheit_to_celsius(self,f):
        f = float(f)
        result = (f - 32) * 5/9
        return result


    def TemperaturaGetEnum(self):
        unity = ["Celsius", "Fahrenheit", "Kelvin"]
        varis = ["Temperatura:"]
        Enum = "Conversor de temperatura\nEntre com o valor da temperatura e selecione a unidade:"
        return varis, Enum, unity

    def Temperatura(self, temp, unity):
        
        temp = float(temp)
        
        if unity == "Celsius":
            f = self.__celsius_to_fahrenheit(temp)
            k = self.__celsius_to_kelvin(temp)

            strshow = "%.2f o Celsius\n%.2f o Fahrenheit\n%.2f o Kelvin" % (temp, f, k)
            return strshow, temp

        #TODO: implement unity == "Fahrenheit" and "Kelvin"
        strshow = "case not implemented"
        return strshow, 0
