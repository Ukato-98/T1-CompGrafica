# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um polígono em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

#from sys import ps1
from ast import Num
from re import A
from typing import List
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
import time

# ***********************************************************************************
Mapa = Polygon()
ConvexHull = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()
PontoClicado = Ponto()

tuplaMapa = []
tuplaConvexHull = []

class Faixa:
    
    def __init__(self):
        self.ArestasNaFaixa = [] # vetor com os ids das arestas que estao na faixa
    
    def CadastraAresta(self, a):
        self.ArestasNaFaixa.append(a) #add um id
    
    def getNroDeArestas(self):
        return len(self.ArestasNaFaixa)
    
    def getAresta(self, i):
        return self.ArestasNaFaixa[i]


class ConjuntoDeFaixas:

    def __init__(self):
        self.TodasAsFaixas =[]
        self.intervalo = 0
        self.inicioFaixas = []

    def SetIntervalo(self, intervalo):
        self.intervalo = intervalo 

    def GetIntervalo(self):
        return self.intervalo
    
    def SetInicioFaixas(self, inicioFaixas):
        self.inicioFaixas = inicioFaixas 

    def GetInicioFaixas(self):
        return self.inicioFaixas

    def CadastraArestaNaFaixa(self, f, a):
        self.TodasAsFaixas[f].CadastraAresta(a)
    
    def CriaFaixas(self, qtdDeFaixas): # pode ser substitu’da por uma construtora
        for i in range(qtdDeFaixas):
            self.TodasAsFaixas.append(Faixa())
    
    def getFaixa(self, f):
        return self.TodasAsFaixas[f]
    

EspacoDividido = ConjuntoDeFaixas()

# ***********************************************************************************
def ImprimeFaixas():
    for i in range(len(EspacoDividido.TodasAsFaixas)):
        print("Faixa:",i,":")
        f = Faixa()
        f = EspacoDividido.getFaixa(i)
        for a in range(f.getNroDeArestas()):
            print(f.getAresta(a)," ")
        print("nro de arestas ", f.getNroDeArestas())
        print("\n")

# ***********************************************************************************
def GeraConvexHull():
    #procura os 4 extremos
    			# *C(-1,0)
	# *D(0,-1)			*B(0,1)
			# *A(1,0)
    import sys
    a = Ponto() # considera os valores mais baixos/altos para depois comparar e reescrever
    b = Ponto()
    c = Ponto()
    d = Ponto()
    # a - n importa, min y
    a.y = sys.maxsize # altera o valor se o pto em comparacao tiver y menor
    # b - max x, n importa
    b.x = -sys.maxsize -1 # altera o valor se o pto em comparacao tiver x maior
    # c - n importa, max y
    c.y = -sys.maxsize -1
    # d - min x, n importa
    d.x = sys.maxsize
    for v in range(Mapa.getNVertices()):
        p = Mapa.getVertice(v)
        if (p.y < a.y): a = p
        if (p.x > b.x): b = p
        if (p.y > c.y): c = p
        if (p.x < d.x): d = p

    # add vetices ao ConvexHull 
    auxConvexHull(a, b, Ponto(1,0,0))
    auxConvexHull(b, c, Ponto(0,1,0)) 
    auxConvexHull(c, d, Ponto(-1,0,0))
    auxConvexHull(d, a, Ponto(0,-1,0))

# ***********************************************************************************
# calcula o menor angulo entre a reta formada pelo pto inicial de ref (a,b,c,d) 
# com os demais vetices do poligono e o vetor base 
def auxConvexHull(ref, final, vetorBase):
    while(not ref == final):
        angulo = 360
        ponto = Ponto()
        for vertice in Mapa.Vertices:
            if not vertice == ref and vertice not in ConvexHull.Vertices:
                vetor = CalculaVetor(ref, vertice)
                auxAngulo = CalculaAngulo(vetor, vetorBase)
                if (auxAngulo < angulo):
                    angulo = auxAngulo
                    ponto = vertice
        ref = ponto
        ConvexHull.insereVertice(ref.x, ref.y, ref.z)    

# ***********************************************************************************
import random
def GeraPontos(qtd):
    file = open(f'Pontos_{qtd}.txt', 'w+')
    
    for i in range(qtd):
        randomX = round(random.uniform(Min.x, Max.x), 6) # .uniform gera numeros com ponto fluturante
        randomY = round(random.uniform(Min.y, Max.y), 6)
        file.write(f'{randomX} {randomY}\n')

    file.close() 

# ***********************************************************************************
def lePontos(filePath) -> List[Ponto]:
    file = open(filePath, "r")
    listaDePontos = []
    for line in file:
        values = line.split(' ')
        if len(values) == 2:
            ponto = Ponto(float(values[0]), float(values[1]), 0)
            listaDePontos.append(ponto)
    return listaDePontos

# ***********************************************************************************
def InterseccaoForcaBruta(listaDePontos):
    contHaInterseccao = 0
    for pontoDir in listaDePontos:
        pontoEsq = pontoDir + Ponto(-1,0) * (abs(Max.x)+100)
        contInterseccoes = 0
        dentro = False
        for n in range(Mapa.getNVertices()):
            verticeInicial, verticeFinal = Mapa.getAresta(n)
            interseccao = HaInterseccao(pontoDir, pontoEsq, verticeInicial, verticeFinal)
            contHaInterseccao+=1
            if (interseccao):
                # interseccao no vertice: como percorre em sentido horário, a interseccao acontece no final da prim aresta. 
                # Em caso do vertice ser o max/min local -> conta 2 interseccoes, uma em cada aresta (pq ele entrou e saiu, ou saiu e entrou)
                # Nos demais vertices, que sao "retos" (fronteiras do poligono, se passou nesse vertice saiu/entrou), só deve contar uma interseccao para as 2 arestas,
                #   entao, diminui 1 do contador quando encontrar a interseccao em uma aresta "reta"
                if (pontoDir.y == verticeFinal.y):
                    verticeInicialProx, verticeFinalProx = Mapa.getAresta((n+1)%Mapa.getNVertices())
                    if (((verticeInicial.y < verticeFinal.y) and (verticeInicialProx.y < verticeFinalProx.y)) 
                        or 
                        ((verticeInicial.y > verticeFinal.y) and (verticeInicialProx.y > verticeFinalProx.y))):
                        contInterseccoes -=1
                contInterseccoes+=1
        dentro = False if contInterseccoes%2 == 0 else True
        tuplaMapa.append((dentro, pontoDir))

    return contHaInterseccao


# ***********************************************************************************
import numpy as np
def InclusaoEmConvexo(listaDePontos):
    # OBS: a ordem das arestas no convex hull esta em sentido anti horario (do Mapa esta em sentido horario)
    # por estar em sentido anti-horario, quando percorremos o convexhull pelas arestas, consideramos que pontos a direita estao fora do poligono
    contProdVetorial = 0
    vetorResultante = Ponto()
    for ponto in listaDePontos:
        dentro = True
        for n in range(ConvexHull.getNVertices()):
            verticeInicial, verticeFinal = ConvexHull.getAresta(n)
            vetorCH = CalculaVetor(verticeInicial, verticeFinal)
            vetorPonto = CalculaVetor(verticeInicial, ponto)
            vetorResultante = ProdVetorial(vetorCH, vetorPonto)
            contProdVetorial+=1
            if (vetorResultante.z < 0):
                dentro = False
                break
        tuplaConvexHull.append((dentro, ponto))
    return contProdVetorial

# ***********************************************************************************
def InclusaoFaixaPorForcaBruta(listaDePontos):
    contHaInterseccao = 0
    for ponto in listaDePontos:
        pontoEsq = ponto+ Ponto(-1,0) * (abs(Max.x)+100)

        #descobrindo a faixa em que o ponto se encontra
        numFaixa = 100
        for indexFaixa, inicioFaixa in enumerate(EspacoDividido.GetInicioFaixas()[:-1]):
            if len(EspacoDividido.GetInicioFaixas()[:-1]) == indexFaixa+1:
                if ponto.y >= inicioFaixa: 
                    numFaixa = indexFaixa
            elif ponto.y >= inicioFaixa and ponto.y <= EspacoDividido.GetInicioFaixas()[indexFaixa+1]: 
                numFaixa = indexFaixa

        contInterseccoes = 0
        for numAresta in EspacoDividido.getFaixa(numFaixa).ArestasNaFaixa:
            verticeInicial, verticeFinal = Mapa.getAresta(numAresta)
            interseccao = HaInterseccao(ponto, pontoEsq, verticeInicial, verticeFinal)
            contHaInterseccao +=1
            if (interseccao):
                # interseccao no vertice: como percorre em sentido horário, a interseccao acontece no final da prim aresta. 
                # Em caso do vertice ser o max/min local -> conta 2 interseccoes, uma em cada aresta (pq ele entrou e saiu, ou saiu e entrou)
                # Nos demais vertices, que sao "retos" (fronteiras do poligono, se passou nesse vertice saiu/entrou), só deve contar uma interseccao para as 2 arestas,
                #   entao, diminui 1 do contador quando encontrar a interseccao em uma aresta "reta"
                if (ponto.y == verticeFinal.y):
                    verticeInicialProx, verticeFinalProx = Mapa.getAresta((numAresta+1)%Mapa.getNVertices())
                    if (((verticeInicial.y < verticeFinal.y) and (verticeInicialProx.y < verticeFinalProx.y)) 
                        or 
                        ((verticeInicial.y > verticeFinal.y) and (verticeInicialProx.y > verticeFinalProx.y))):
                        contInterseccoes -=1
                   
                contInterseccoes+=1           
        dentro = False if contInterseccoes%2 == 0 else True
    return contHaInterseccao

# ***********************************************************************************
def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ***********************************************************************************
def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Seleção, com 10% das dimensões do polígono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ***********************************************************************************
def display():
    global PontoClicado

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0, 0, 1.0)
    Mapa.desenhaPoligono()

    # glColor3f(0, 1.0, 0)
    # ConvexHull.desenhaVertices()
    glColor3f(1, 1.0, 0)
    ConvexHull.desenhaPoligono()

    glColor3f(1.0, 0.0, 0.0)
    

    # desenha faixas
    for y in EspacoDividido.GetInicioFaixas(): 
        glColor3f(1,0,1)
        Pinicial = Ponto(Min.x,y)
        Pfinal = Ponto(Max.x,y)
        DesenhaLinha(Pinicial,Pfinal)
    
    
    # desenha pontos de acordo com a inclusao no poligno de exemplo e no convex hull
    for index, (dentroM, ponto) in enumerate(tuplaMapa):
        (dentroCH, ponto) = tuplaConvexHull[index]
        glPointSize(5)
        glBegin(GL_POINTS)

        glColor3f(1,0,0) 
        glVertex3f(ponto.x,ponto.y,ponto.z)
        if dentroCH:
            glColor3f(1,1,0)
            glVertex3f(ponto.x,ponto.y,ponto.z)

        if dentroM:
            glColor3f(0,0,1)
            glVertex3f(ponto.x,ponto.y,ponto.z)
        glEnd()


    #Mapa.desenhaVertices()
    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b'p':
        Mapa.imprimeVertices()
    if args[0] == b'a':
        Mapa.LePontosDeArquivo("EstadoRS.txt")
    if args[0] == b'1':
        P1, P2 = Mapa.getAresta(9)
        P1.imprime()
        P2.imprime()

# Força o redesenho da tela
    glutPostRedisplay()
# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        pass

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)

    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************


Min, Max = Mapa.LePontosDeArquivo("PoligonoDeTeste2.txt")


GeraPontos(20)
# GeraPontos(200)
# GeraPontos(2000)
# GeraPontos(20000)


Min.x -= 1
Min.y -= 1
Max.x += 1
Max.y += 1

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Exibe Polignos")
glutDisplayFunc(display)
#glutIdleFunc(showScreen)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)




GeraConvexHull()

# --------FAIXAS----------
EspacoDividido.CriaFaixas(10)
# P1 = Ponto()
# P2 = Ponto()

import numpy as np
start, end =  Mapa.getLimits()
intervalo = (abs((end.y)-(start.y)))/len(EspacoDividido.TodasAsFaixas)
EspacoDividido.SetIntervalo(intervalo)

faixasInicio = np.arange(start.y, end.y, intervalo)
faixasInicio = np.append(faixasInicio, end.y)
EspacoDividido.SetInicioFaixas(faixasInicio)

# Cadastrando aresta na faixa
for i in range(Mapa.getNVertices()):
    P1,P2 = Mapa.getAresta(i)

    inicioFaixa = P1.y
    fimFaixa = P2.y 


    if(fimFaixa<inicioFaixa):
        inicioFaixa, fimFaixa = fimFaixa, inicioFaixa
    
    nroFaixaInicio = -10
    for faixaNum in range(len(EspacoDividido.TodasAsFaixas)):
        limites = EspacoDividido.GetInicioFaixas()
        if inicioFaixa >= limites[faixaNum] and inicioFaixa < limites[faixaNum+1]:
            nroFaixaInicio = faixaNum
            break
    
    nroFaixaFim = -10
    for faixaNum in range(len(EspacoDividido.TodasAsFaixas)):
        limites = EspacoDividido.GetInicioFaixas()
        if fimFaixa >= limites[faixaNum] and fimFaixa <= limites[faixaNum+1]:
            nroFaixaFim = faixaNum
            break
    
    for f in range (nroFaixaInicio, nroFaixaFim+1):
        EspacoDividido.CadastraArestaNaFaixa(f, i)


# ImprimeFaixas()
# ------------------

listaP = lePontos("PontosDeTeste2.txt")

# algoritmos
timeInit= time.time()
contadorHaInterseccao = InterseccaoForcaBruta(listaP)
timeFinal= time.time() - timeInit
print(f'TEMPO DE EXECUÇÃO ALGORITMO FORCA BRUTA {round(timeFinal, 6)} ms')
print(f'Funcao HaInterseccao foi chamada {contadorHaInterseccao} vezes')

print("\n ")

timeInit= time.time()
contadorProdVetorial = InclusaoEmConvexo(listaP)
timeFinal= time.time() - timeInit
print(f'TEMPO DE EXECUÇÃO ALGORITMO DE INCLUSAO EM CONVEXO {round(timeFinal, 6)} ms')
print(f'Funcao ProdVetorial foi chamada {contadorProdVetorial} vezes')

print("\n ")

timeInit= time.time()
contadorHaInterseccao = InclusaoFaixaPorForcaBruta(listaP)
timeFinal= time.time() - timeInit
print(f'TEMPO DE EXECUÇÃO ALGORITMO FORCA BRUTA CONSIDERANDO FAIXAS {round(timeFinal, 8)} ms')
print(f'Funcao HaInterseccao foi chamada {contadorHaInterseccao} vezes')

try:
    glutMainLoop()
except SystemExit:
    pass
