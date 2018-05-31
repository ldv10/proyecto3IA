# -*- coding: utf-8 -*-
"""
Created on Sun May 20 20:04:54 2018

@author: Leonel Guillen
"""

board1 = [0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 2, 0, 0, 0,
        0, 0, 0, 2, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0]
#arriba,abajo, izquierda, derecha, arriba_derecha, abajo_derecha, abajo_izquierda, arriba_izquierda
direcciones = [-10,10,-1,1,-9,11,9,-11]

#Casillas que seran usables en el nuevo formato
usables = [11,12,13,14,15,16,17,18,
21,22,23,24,25,26,27,28,
31,32,33,34,35,36,37,38,
41,42,43,44,45,46,47,48,
51,52,53,54,55,56,57,58,
61,62,63,64,65,66,67,68,
71,72,73,74,75,76,77,78,
81,82,83,84,85,86,87,88]


pesos = [0,0,0,0,0,0,0,0,0,0,
 0,9,6,3,3,3,3,6,9,0,
 0,6,1,1,1,1,1,1,6,0,
 0,3,1,1,1,1,1,1,3,0,
 0,3,1,1,1,1,1,1,3,0,
 0,3,1,1,1,1,1,1,3,0,
 0,3,1,1,1,1,1,1,3,0,
 0,6,1,1,1,1,1,1,6,0,
 0,9,3,3,3,3,3,3,9,0,
 0,0,0,0,0,0,0,0,0,0]



#Parsea el board para nuestro algoritmo
def boardParser(board):
    x = usables
    new = ['|']*100
    pos_board = 0
    for i in x:
        new[i] = board[pos_board]
        pos_board = pos_board + 1
    return new


#Nos indica quien es el jugador rival
def rival(jugador):
    if jugador == 1:
        return 2
    else:
        return 1

#Me devuelve las casillas donde El jugador tienesus fichas.
def ubicacion(jugador,board):
    ubi = []
    con = 0
    for i in board:
        if i == jugador:
            ubi.append(con)
        con = con + 1
    return ubi

#Me da los movimientos validos
def movVal(jugador,board):
    #en legales se guarda los mivimientos para el tablero parseado
    legales = []
    #Representacion de fichas rivales
    riv = rival(jugador)
    #primero encuentro mis fichas
    fichas = ubicacion(jugador,board)
    #exploramos direcciones de cada ficha
    for i in fichas:
        for x in direcciones:
            #Se obtienen las direcciones
            valido = i + x
            while board[valido] == riv:
                valido = valido + x
                #Verifica que OX(x2)O que (x2) no la tome en blanco cuando es rival
                if board[valido] != riv and board[valido] != '|' and board[valido] != jugador:
                    #verifica que sea unico
                    if valido not in legales:
                        legales.append(valido)
    return legales


def moveParser(jugador, board):
    legales = movVal(jugador,board)
    #en reales se guardan los movimientos validos para el protocolo
    reales = []
    #El contador nos va a servir para contar los '|' antes de cada ficha
    contador = 0
    for a in legales:
        for q in range(a):
            if board[q] == '|':
                contador = contador + 1
        reales.append(a-contador)
        contador = 0
    return reales

def parser(mov,board):
    contador = 0
    real = 0
    for a in range(mov + 1):
        if board[a] == '|':
                contador = contador + 1
        real = a - contador
    return real


#Funcion que nos simula un tiro, me regresa un board
def movimiento(mov,jugador,board):
    board[mov] = jugador
    #Ponemos la ficha en la casilla que corresponde
    riv = rival(jugador)
    #Analiza las direcciones con la condicion de que a su alrededor haya una rival
    # y que despues de esta siga la rival o una de nosotros (para evitar que solo si hay rival ponga)
    for x in direcciones:
        kill = mov + x
        if board[kill] == riv:
            while board[kill] != 0 and (board[kill+x] == jugador or board[kill+x] == riv):
                board[kill] = jugador
                kill = kill + x
    return board


#Heuristicas______________________________________________________________________________
#Heuristica1
#Asigna valor de utilidad en base a la cantidad de las piezas que de un jugador.
#Es decir que esta heuristica busca hacer el tiro que capture mas piezas.

def heur1(jugador,board):
    #contadores de piezas
    jug = 0
    riv = 0
    jug2 = rival(jugador)
    for i in usables:
        if board[i] == jugador:
            jug = jug + 1
            #print("JUG encontrado en ", i)
        elif board[i] == jug2:
            riv = riv + 1
            #print("RIV encontrado en ", i)
    return jug - riv

def pickheur(jugador,board):
    jug = 0
    riv = 0
    jug2 = rival(jugador)
    for i in usables:
        if board[i] == jugador:
            jug = jug + 1
            #print("JUG encontrado en ", i)
        elif board[i] == jug2:
            riv = riv + 1
            #print("RIV encontrado en ", i)
    return jug + riv

def heur2(jugador,board):
    riv = rival(jugador)
    contador = 0
    for i in usables:
        if board[i] == jugador:
            contador = contador + pesos[i]
        elif board[i] == riv:
            contador = contador - pesos[i]
    return contador

#_________________________________________________________________________________

def tiro(player,board,depth,evaluate):
    tiro = minimax(player,board,depth,evaluate,0)
    return tiro[1]

def tiroAlfa(player,board,depth,evaluate):
    tiro = alfabeta(player,board,depth,-100000,100000,heur2,0)
    return tiro[1]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ALGORITMOS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Minimax
def minimax(jugador, board, depth, heuristica, actual):
    #Si ya igualamos donde estamos con la profundidad, solo nos devuelve el valor asignado por la heuristica.
    if actual == depth:
        return heuristica(jugador, board), None
    #Sacamos los movimientos validos
    moves = movVal(jugador, board)
    #Si ya no hay movimientos, saca el valor del tablero
    if not moves:
        return minimax(rival(jugador), board, depth, heuristica,actual + 1)[0], None
    #Explicacion: si estoy en 0 mod 2, simulo el tiro del rival, dado los tableros generados por mi movimiento dado, profundidad, evaluate y actual se mantienen
    #Si es 0 en mod 2 significa que es nuestro turno y queremos maximisar
    if actual % 2 == 0:
        maxEval = -10000000 #Peor valor que se puede obtener,
        for m in moves: #Se evalua cada movimiento
            #se pone negativo porque como es el tablero rival, su scorsera el negativo para nosotros.
            evalu = -minimax(rival(jugador), movimiento(m, jugador, list(board)), depth, heuristica,actual + 1)[0]
            maxEval=max(maxEval,evalu)#maximo
            #print(maxEval)
        return (maxEval,m)
    #Caso contrario es el turno del rival y el quiere minimizar
    else:
        minEval = 10000000
        for m in moves:
            evali = minimax(jugador, movimiento(m, rival(jugador), list(board)), depth, heuristica,actual + 1)[0]
            minEval = min(minEval,evali)
        return (minEval,evali)


def alfabeta(jugador, board, depth, alfa, beta, heuristica, actual):
    #Si ya igualamos donde estamos con la profundidad, solo nos devuelve el valor asignado por la heuristica.
    if actual == depth:
        return heuristica(jugador, board), None
    #Sacamos los movimientos validos
    moves = movVal(jugador, board)
    #Si ya no hay movimientos, saca el valor del tablero
    if not moves:
        return alfabeta(rival(jugador), board, depth, alfa, beta, heuristica,actual + 1)[0], None
    #Explicacion: si estoy en 0 mod 2, simulo el tiro del rival, dado los tableros generados por mi movimiento dado, profundidad, evaluate y actual se mantienen
    #Si es 0 en mod 2 significa que es nuestro turno y queremos maximisar
    if actual % 2 == 0:
        maxEval = -10000000 #Peor valor que se puede obtener,
        for m in moves: #Se evalua cada movimiento
            #se pone negativo porque como es el tablero rival, su scorsera el negativo para nosotros.
            evalu = -alfabeta(rival(jugador), movimiento(m, jugador, list(board)), depth, alfa, beta, heuristica,actual + 1)[0]
            maxEval=max(maxEval,evalu)#maximo
            alfa = max(alfa,evalu)
            if beta <= alfa:
                break
            #print(maxEval)
        return (maxEval,m)
    #Caso contrario es el turno del rival y el quiere minimizar
    else:
        minEval = 10000000
        for m in moves:
            evali = alfabeta(jugador, movimiento(m, rival(jugador), list(board)), depth, alfa, beta, heuristica,actual + 1)[0]
            minEval = min(minEval,evali)
            beta = min(beta,evali)
            if beta <= alfa:
                break
        return (minEval,evali)




parIni = ['|','|','|','|','|','|','|','|','|','|',
 '|',0,0,0,0,0,0,0,0,'|',
 '|',0,0,0,0,0,0,0,0,'|',
 '|',0,0,0,5,0,0,0,0,'|',
 '|',0,0,0,1,2,0,0,0,'|',
 '|',0,0,0,2,1,0,0,0,'|',
 '|',0,0,0,0,0,0,0,0,'|',
 '|',0,0,0,0,0,3,0,0,'|',
 '|',0,0,0,0,0,0,0,0,'|',
 '|','|','|','|','|','|','|','|','|','|']


pr = ['|','|','|','|','|','|','|','|','|','|',
 '|',1,1,1,1,1,1,1,2,'|',
 '|',1,1,1,1,1,1,1,2,'|',
 '|',1,1,1,1,1,1,1,2,'|',
 '|',1,1,1,1,1,1,0,2,'|',
 '|',1,1,2,2,1,1,0,0,'|',
 '|',2,1,1,2,1,1,0,0,'|',
 '|',2,2,2,1,1,1,0,0,'|',
 '|',2,1,0,0,1,0,0,0,'|',
 '|','|','|','|','|','|','|','|','|','|']

