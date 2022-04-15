# ************************************************
#   Ponto.py
#   Define a classe Ponto
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

""" Classe Ponto """
# from typing import TypeAlias


from typing import Tuple

from numpy import true_divide


class Ponto:   
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
    
    """ Comparar 2 objetos de uma mesma classe """
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else: False

    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            print (msg, self.x, self.y, self.z)
        else:
            print (self.x, self.y, self.z)

    """ Define os valores dos eixos do ponto """
    def set(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
# Definicao de operadores
# https://www.programiz.com/python-programming/operator-overloading
    def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            return Ponto(x, y)

    def __mul__(self, other: int):
            x = self.x * other
            y = self.y * other
            return Ponto(x, y)

# **********************************************************************
#    Calcula o produto escalar entre os vetores V1 e V2
# **********************************************************************
def ProdEscalar(v1: Ponto, v2: Ponto) -> float:
    return v1.x*v2.x + v1.y*v2.y+ v1.z*v2.z

def ProdVetorial (v1: Ponto, v2: Ponto) -> Ponto:
    vresult = Ponto()
    vresult.x = v1.y * v2.z - (v1.z * v2.y)
    vresult.y = v1.z * v2.x - (v1.x * v2.z)
    vresult.z = v1.x * v2.y - (v1.y * v2.x)
    return vresult

import math
def Modulo (v1: Ponto) -> float:
    return math.sqrt(v1.x**2 + v1.y**2 + v1.z**2)

def CalculaAngulo(v1: Ponto, v2: Ponto) -> float:
    x = ProdEscalar(v1,v2) / (Modulo(v1)*Modulo(v2))
    x = round(x,2)
    return math.degrees(math.acos(x))

# calculo eh ponto da seta - ponto da "base" do vetor
# p1 eh base, p2 eh seta
def CalculaVetor(p1: Ponto, p2: Ponto) -> Ponto:
    return Ponto(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)


# ********************************************************************** */
#                                                                        */
#  Calcula a interseccao entre 2 retas (no plano "XY" Z = 0)             */
#                                                                        */
# k : ponto inicial da reta 1                                            */
# l : ponto final da reta 1                                              */
# m : ponto inicial da reta 2                                            */
# n : ponto final da reta 2                                              */
# 
# Retorna:
# 0, se não houver interseccao ou 1, caso haja                                                                       */
# int, valor do parâmetro no ponto de interseção (sobre a reta KL)       */
# int, valor do parâmetro no ponto de interseção (sobre a reta MN)       */
#                                                                        */
# ********************************************************************** */
def intersec2d(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> Tuple[int, float, float]:
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None # não há intersecção

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

# **********************************************************************
# HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto)
# Detecta interseccao entre os pontos
#
# **********************************************************************
def HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0

