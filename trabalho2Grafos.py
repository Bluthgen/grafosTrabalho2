# -*- coding: utf-8 -*-
import math
import sys
import heapq
import queue


class Vertice:
    def __init__(self, nome:int, coords:tuple):
        self.nome= nome
        self.x, self.y= coords
        self.chave= math.inf
        self.pai = 0
        self.filhos = []
        

    @staticmethod
    def distance(v1, v2):
            return math.hypot(v2.x - v1.x, v2.y - v1.y)
        
    def __lt__(self, outro):
        return self.chave < outro.chave
    
    def __repr__(self):
        return f'{self.nome}'

class GrafoCartesiano:
    def __init__(self):
        self.vertices= []
        
    def add(self, v):
        if isinstance(v, Vertice):
            self.vertices.append(v)
            
   
class No:
    def __init__(self):
        self.filhos= {}
        
    def add(self, v: Vertice, nome: int):
        if not v in self.filhos:
            self.filhos[nome]= v;

def prim(grafo,s):
    s.chave = 0
    pq = [(v.chave,v) for v in grafo.vertices]
    heapq.heapify(pq)
    while len(pq) > 0:
        currentVert = heapq.heappop(pq)
        if currentVert[0] != currentVert[1].chave:
            continue
        for nextVert in grafo.vertices:
            if nextVert == currentVert or nextVert == s:
                continue
            newCost = Vertice.distance(currentVert[1],nextVert)
            if (nextVert.chave, nextVert) in pq and newCost<nextVert.chave:
                if nextVert.pai != 0:
                    nextVert.pai.filhos.remove(nextVert.nome - 1)
                nextVert.pai = currentVert[1]
                currentVert[1].filhos.append(nextVert.nome-1)
                nextVert.chave = newCost
                heapq.heappush(pq, (newCost, nextVert))
   
def visitaEmProfundidade(grafo, u, lista):
    lista.append(u)
    if grafo.vertices[u].filhos != []:
        for i in grafo.vertices[u].filhos:
            visitaEmProfundidade(grafo, i, lista)

def solucaoInicial(grafo: GrafoCartesiano, s: int):
    solucao = [s]
    for i in grafo.vertices[s].filhos:
        visitaEmProfundidade(grafo, i, solucao)
    return solucao
    
def doisOpt(solucao, grafo: GrafoCartesiano):
    n = len(solucao)
    troca1 = troca2 = 0
    while True:
        ðmax = 0
        for u in range(0, n-2):
            if u == 0:
                limite = n-1
            else:
                limite = n
            v = u+1
            if not u+2 > limite:
                for x in range(u+2, limite):
                    if x == n-1:
                        y= 0
                    else:
                        y= x+1
                    ð= (Vertice.distance(grafo.vertices[solucao[u]],grafo.vertices[solucao[v]]) + Vertice.distance(grafo.vertices[solucao[x]],grafo.vertices[solucao[y]])) - (Vertice.distance(grafo.vertices[solucao[u]],grafo.vertices[solucao[x]]) + Vertice.distance(grafo.vertices[solucao[v]], grafo.vertices[solucao[y]]))
                    if ð > ðmax:
                        ðmax = ð
                        troca1 = v
                        troca2 = x
        if ðmax > 0:
            aux= []
            for k in range(troca1, troca2+1):
                aux.append(solucao[k])
            aux.reverse()
            for k in range(troca1, troca2+1):
                solucao[k]= aux[k - troca1]
            troca1 = troca2 = 0                
        else:
            return solucao
    

def inicializaCartesiano():    
    grafo= GrafoCartesiano()
    with open("Testes/burma14.tsp", "r") as arquivo:
        for linha in arquivo:
            params= linha.split(" ")
            nome= params[0]
            coords1= params[1]
            coords2= params[2]
            coords= (float(coords1), float(coords2))
            grafo.add(Vertice((int (nome)), coords))
    return grafo

grafo = inicializaCartesiano()
s= 0
prim(grafo, grafo.vertices[s])

solucao = solucaoInicial(grafo, s)

#solucao = doisOpt(solucao, grafo)
custo = 0
for i in solucao:
    if i == len(solucao)-1:
        custo = custo + Vertice.distance(grafo.vertices[solucao[i]], grafo.vertices[solucao[0]])
    else:
        custo = custo + Vertice.distance(grafo.vertices[solucao[i]], grafo.vertices[solucao[i+1]])
        
print(custo, ":", sep="", end=" ")
for i in solucao:
    print(solucao[i], end=" ")