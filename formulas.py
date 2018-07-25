"""
Created on 21 de jul de 2018

@author: Ryan Gazaniga <ryangazaniga@gmail.com>

Proposito: Classe myFormula disponibiliza funcoes para calculos de formulas fisicas e matematicas.
           As funcoes devem ser padronizadas e possuir implementacao de NomeFormula() e NomeFormulaGetEnum()
           
           Uma funcao GetEnum necessita do seguinte padrao
            
            varis = ["Var1:", "Var2:", "Var3:"] # MAX 3 campos 
            unity = ["unidade1", "unidade2"] # MAX 3 campos 
            Enum = "Titulo breve. Defina os dados:"
           
           A funcao GetEnum retorna os dados da seguinte maneira
           
               return varis, Enum, unity 
           
           Uma funcao de calculo de formula necessita do seguinte padrao
           
            -> Ser definida com ate 3 variaveis e caso tenha definido unity em GetEnum, precisa do unity

               def NomeFormula(self, var1, var2, var3, unity):
          
            -> Formatar as variaveis recebidas como string
                var1 = float(var1)
        
            -> Fazer o calculo na variavel result
                result = var1 + var2 * var3
            
            -> Definir deducao da formula para apresentar ao calculo na variavel strshow
                strshow = "S = %.2f + %.2f * %.2f\nS = %.2f + %.2f\nS = %.2f" % (s0, V, T, s0, (V*T), result)
            
            -> Retornar as variaveis com resultado e output para o usuario
                return strshow, result
"""

# Include inportant math libs such as:
#   pow,sqrt,log
#   sin,cos, etc
import math

"""
Class myFormula 

Mandatory methods:
    Formula(self,var1,var2) # MAX 3 Variables
        Must return strshow, result

    FormulaGetEnum(self)
        Must return varis, Enum, unity # unity can be void, unity = []

Optional Methods
    Convert(self, self, valor, unit, unitToConvert)

If you want to hide your method from the combobox list 
begin the method's name with __

other methods like __init__, Convert and GetEnum are hidden.

eg:

    __celsius_to_kelving(self, c)


"""
class myFormula:
    def __init__(self):
        pass
    

    # Hidden Functions to calculate de temperature
    # To be used on Temperatura and Converter
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

 
    def vmediaGetEnum(self):
        unity = ["km/h", "m/s", "mph"]
        varis = ["Variacao de espaco", "Intervalo de tempo"]
        Enum = "Calculo de velocidade escalar media.\nVm = Delta S / Delta T. Defina os dados:"
        return varis, Enum, unity 

    def vmedia(self, s, t, unity):
        s = float(s)
        t = float(t)
        result = s / t
        strshow = "S = %.2f / %.2f\nS = %.2f %s" % (s, t, result, unity)

        return strshow, result

    def EqHorariaGetEnum(self):
        varis = ["Espaco incial:", "Velocidade:", "Tempo:"]
        unity = ["km/h", "m/s", "mph"]
        Enum = "Calculo de espaco percorrido em MRU.\nS = S0 + V * T. Defina os dados:"
        return varis, Enum, unity
     
    def EqHoraria(self, s0, V, T, unity):
        
        s0 = float(s0)
        V  = float(V)
        T  = float(T)
        
        result = s0 + V * T
        strshow = "S = %.2f + %.2f * %.2f\nS = %.2f + %.2f\nS = %.2f %s" % (s0, V, T, s0, (V*T), result, unity)
        
        return strshow, result

    #TODO: Criar formulas deduzidas para calculo de outras variaveis da formula.  
    def EqHorariaS0GetEnum(self):
        varis = ["Espaco Percorrido:", "Velocidade:", "Tempo:"]
        unity = ["km/h", "m/s", "mph"]
        Enum = "Espaco inicial em MRU.\nS = S0 + V * T. Defina os dados:"
        return varis, Enum, unity
           
    #TODO: Criar formulas deduzidas para calculo de outras variaveis da formula.  
    def EqHorariaS0(self, s, V, T, unity):
        
        s = float(s)
        V  = float(V)
        T  = float(T)
        
        #FIXME: Ajustar/deduzir equacao para calculo de S0
        result = s + V * T
        strshow = "S0 = %.2f + %.2f * %.2f\nS = %.2f + %.2f\nS = %.2f %s" % (s, V, T, s, (V*T), result, unity)
        
        return strshow, result
    
    '''
    Funcao de conversao de medidas
    E necessario implementar a condicao considerando que valor deve ser 
    convertido, unit e a unidade de medida atual e unitToConvert 
    e a unidade para qual valor sera convertido.
    Se a condicao nao for satisfeita sera retornado -1
    '''
    def Converter(self, valor, unit, unitToConvert):
        
        if  unit == "km/h" and unitToConvert == "m/s":
            return valor / 3.6
        
        elif unit == "m/s" and unitToConvert == "km/h":
            return valor * 3.6
        
        #TODO:  elif unit == "km/h" and unitToConvert == "mph":
        #Multiplica o valor em MPh por 1,60934 e achara em Km/h

        #TODO:  elif unit == "mph" and unitToConvert == "km/h":
        #Multiplica o valor em MPh por 1,60934 e achara em Km/h

        return -9999
        
    def pitagoras(self, a, b, c):
        
        a = float(a)
        b = float(b)
        c = float(c)
        
        if a == 0:
            
            # a2 = b2 + c2
            # a = sqrt(pow(b,2),pow(c,2)) # can be used for any pow eg.: pow(3,4) = 3*3*3*3
            result = math.sqrt(math.pow(b, 2) + math.pow(c,2))

        #TODO: if b == 0: 
        #TODO: if c == 0:
        
        strshow = str(result)
                
        return strshow, result
    
    def pitagorasGetEnum(self):
        varis = ["Hipotenusa a:", "Cateto b:", "Cateto c:"]  
        unity = []  
        Enum = "Teorema de Pitagoras escolha duas variaveis e a 3a sera exibida:"  
        return varis, Enum, unity
        
    
    
    
