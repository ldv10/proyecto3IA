# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 08:49:50 2018

@author: ldv
mi ip 10.76.94.20
"""

import socketIO_client
import random as ran
from funciones import boardParser, movVal, tiro, heur1,parser,moveParser,heur2,pickheur, tiroAlfa

goldmoves = [11,18,81,88]

#Me devuelve las esquinas
def goldMov(jugador,board):
    tiro = 0
    for i in movVal(jugador,board):
        if i in goldmoves:
            tiro = i
            break
    return tiro

#10.43.64.164 4000
#
#tournament_id = 142857
tournament_id = 142857
#s = socketIO_client.SocketIO("192.168.5.162", 4000)
s = socketIO_client.SocketIO("192.168.1.142", 4000)
jugador = "Leonel"
s.connect()
s.emit('signin',
       {'user_name': jugador,
        'tournament_id': tournament_id,
        'user_role': 'player'})


def connected():
    print('Login succesful')

def end(y):

    s.emit('player_ready', {
    'tournament_id': tournament_id,
    'game_id': y['game_id'],
    'player_turn_id': y['player_turn_id']
  })
    ganador = "winner_turn_id"
    if ganador in y:
        if y["player_turn_id"] == y["winner_turn_id"]:
            print("Gano mi IA +++++++++++++++++++++++++++++++++++++++++++++++++++++++", jugador)
        else:
            print("Perdio mi IA -----------------------------------------------------", jugador)

def play(y):
    print("Ready!")
    #x =  ran.randint(0,63)
    board = y['board']
    parseado = boardParser(board)
    jugador = y['player_turn_id']
    print("Soy el jugador: ", jugador)
    gold = goldMov(jugador,parseado)
    if gold == 0:
        totPiezas = pickheur(jugador,parseado)
        if totPiezas <=20:
            t = tiroAlfa(jugador,parseado,4,heur2) #minimax con heuristica1 (de piezas)
            #t = tiro(jugador,parseado,5,heur1)
            tiro1 = parser(t,parseado)
            print("Tiro bueno con alfabeta heurisitca 2")
        elif totPiezas > 20:
            t = tiroAlfa(jugador,parseado,4,heur2)
            #t = tiro(jugador,parseado,5,heur1) #minimax con heuristica1 (de piezas)
            tiro1 = parser(t,parseado)
            print("Tiro bueno con minimax heuristica 1")
    else:
        tiro1 = parser(gold,parseado)
        print("Esquina ganada!!!___________________________")
    s.emit('play',
           { 'tournament_id': tournament_id,
    'player_turn_id': y['player_turn_id'],
    'game_id': y['game_id'],
    'movement': tiro1
  })



s.on('ok_signin', connected)
s.on('ready',play)
s.on('finish',end)

s.wait()


