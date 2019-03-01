# -*- coding: utf-8 -*-
"""
#!/usr/bin/env python
Created on Fri Mar  1 09:01:05 2019

@author: JC056596
"""
import random
import sys

class Game(object):
    def __init__(self, ai1, ai2):
        self.ai1 = ai1
        self.ai2 = ai2
        self.ai1Wins = 0
        self.ai2Wins = 0
        self.resetBoard()
        self.winningPatterns = [[0,3,6],[1,4,7],[2,5,8],[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6]] #three in a rows
        self.convert = {0:" ", 1: "X", -1:"O"}
    
    def play(self):
        notFilled = 9
        self.resetBoard()
        turn = bool(random.getrandbits(1))
        while(notFilled > 0):
            if turn:
                if not self.fill(self.ai1.choice(self.board), 1): #1 stands for "x"
                    #invalid move, they automatically lose
                    self.ai2Wins+=1
                    return -1
            else:
                if not self.fill(self.ai2.choice(self.inverted_board), -1): #-1 stands for "o"
                    #invalid move, they automatically lose
                    self.ai1Wins+=1
                    return 1
            
            turn = not turn
            notFilled-=1
            winner = self.findWinner()
            
            if winner!=0:
                if winner == 1:
                    self.ai1Wins+=1
                else:
                    self.ai2Wins+=1
                return winner
        return 0
    
    def play_many_games(self, n):
        for i in range(n):
            self.play()
    
    def resetBoard(self):
        self.board = [0 for i in range(9)]
        self.inverted_board = [0 for i in range(9)]
        
    def fill(self, position, val):
        if(self.board[position] != 0):
            return False
        self.board[position] = val
        self.inverted_board[position] = -val
        return True
        
    def findWinner(self):
        #search through patterns to find the winner
        for group in self.winningPatterns:
            if self.board[group[0]] != 0 and self.board[group[0]] == self.board[group[1]] and self.board[group[0]] == self.board[group[2]]:
                return self.board[group[0]]
        return 0
            
    def __str__(self):
        return (u"\n\u2014\u2014\u2014\u2014\u2014\n").join("|".join(self.convert[self.board[x]] for x in range(i*3, i*3 + 3)) for i in range(3))
    
    
class Ai(object):
    pass
class TicTacToeAi(Ai):
    def __init__(self, algorithm = None):
        if algorithm == None:
            algorithm = [[[random.random() for i in range(9)] for _ in range(2)] for j in range(9)]
        
        self.algorithm = algorithm
        
    def choice(self, board):
        outputs = [sum(board[i]*weights[i] + offsets[i] for i in range(9)) for weights, offsets in self.algorithm]
        return outputs.index(max(outputs))
    
    def mutate(self, variation1 = 0.1, variation2 = 0.1):
        for weights, offsets in self.algorithm:
            for i in range(9):
                weights[i] += random.random()*2*variation1 - variation1
                offsets[i] += random.random()*2*variation2 - variation2
                

def cross(ai1, ai2):
    return TicTacToeAi([[[(ai1.algorithm[j][k][i] + ai2.algorithm[j][k][i])/2 for i in range(9)] for k in range(2)] for j in range(9)])

class DefaultAi(Ai):
    def choice(self, board):
        return int(random.random()*9)

default_ai = DefaultAi()
ais = [TicTacToeAi() for i in range(20)]
for i in range(1):
    scores = []
    for ai in ais:
        game = Game(ai, default_ai)
        game.play_many_games(100)
        scores.append(game.ai1Wins)
    
    sorted_ais = tuple(zip(*sorted(tuple(zip(ais, scores)), key = lambda x: x[1])))[0]  #sort by scores
    ais = list(sorted_ais[-10:])
    for j in range(10):
        ais.append(cross(random.choice(ais), random.choice(ais)))

    ai1 = ais[10]
    game = Game(ai1, default_ai)
    game.play()
    #print(game)
    #print()