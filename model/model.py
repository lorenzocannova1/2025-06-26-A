import copy
from datetime import datetime

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self._bestScore = 0
        self._optListCircuiti = []

    def defAllDateCampionato(self):
        return DAO.defAllDateCampionato()

    def creaGrafo(self, da, a):
        nodi = DAO.getAllCircuiti()
        self.grafo.add_nodes_from(nodi)
        for nodo in nodi:
            for i in range(da, a+1):
                res = DAO.getResByCircuit(i, nodo.circuitId)
                if len(res) > 0:
                    nodo.results[i] = res

        for i in nodi:
            for j in nodi:
                if i.circuitId < j.circuitId and self.calcolaPesoArco(i,j) > 0:
                    self.grafo.add_edge(i, j, weight=self.calcolaPesoArco(i, j))

    def calcolaPesoArco(self, i, j):
        peso = 0
        if len(i.results) == 0 or len(j.results) == 0:
            return peso

        for a in i.results.values(): #per ogni anno
            for p in a: # per ogni pilota
                if p.position is not None:
                    peso += 1

        for a in j.results.values():  # per ogni anno
            for p in a:  # per ogni pilota
                if p.position is not None:
                    peso += 1

        return peso

    def getInfoGrafo(self):
        nNodi = len(self.grafo.nodes)
        nArchi = len(self.grafo.edges)

        return nNodi, nArchi

    def componenteConnessaMaggiore(self):
        Tuttecc = list(nx.connected_components(self.grafo))
        Tuttecc.sort(key=lambda x: len(x), reverse=True)
        cc = Tuttecc[0]
        res = []
        for c in cc:
            nodi = self.grafo.neighbors(c)
            val = 0
            for n in nodi:
                if self.grafo[c][n]["weight"] > val:
                    val = self.grafo[c][n]["weight"]
            res.append( (c, val) )

        res.sort(key=lambda x:x[1], reverse=True)
        return res

    def getCampionatoIdeale(self, soglia, numAnni):
        tic = datetime.now()
        self._bestScore = 0
        self._optListCircuiti = []
        Tuttecc = list(nx.connected_components(self.grafo))
        Tuttecc.sort(key=lambda x: len(x), reverse=True)
        cc = Tuttecc[0]

        parziale = []
        rimanenti = copy.deepcopy(cc)

        for c in cc:
            if len(list(c.results.keys())) >= numAnni:
                parziale.append(c)
                rimanenti.remove(c)
                self.ricorsione(parziale, rimanenti, soglia, numAnni)
                parziale.pop()
                rimanenti.add(c)

        listOfScores = []
        for c in self._optListCircuiti:
            listOfScores.append(self.calcolaIndiceCircuito(c))

        toc = datetime.now()
        print(f"Tempo di esecuzione: {toc - tic}")
        return self._optListCircuiti, self._bestScore, listOfScores

    def ricorsione(self, parziale, rimanenti, soglia, numAnni):
        if len(parziale) == soglia:
            # questa fa sia da condizione di ottimalità sia da condizione di terminazione
            if self.getScoreSoluzione(parziale) > self._bestScore:
                self._bestScore = self.getScoreSoluzione(parziale)
                self._optListCircuiti = copy.deepcopy(parziale)
            return

        for c in rimanenti:
            if len(list(c.results.keys())) >= numAnni:
                parziale.append(c)
                rimanenti.remove(c)
                self.ricorsione(parziale, rimanenti, soglia, numAnni)
                parziale.pop()
                rimanenti.add(c)

    def getScoreSoluzione(self, listOfCircuits):
        listOfScores = []
        for c in listOfCircuits:
            listOfScores.append(self.calcolaIndiceCircuito(c))

        return sum(listOfScores)

    def calcolaIndiceCircuito(self, circuito):
        nP = 0
        nPtot = 0

        if len(circuito.results.values()) == 0:
            return 0  # questo caso non dovrebbe mai accadere perchè questa funzione viene chiamata solo su nodi appartenenti alla componente connessa.

        for r in circuito.results.values():  # per ogni anno prendo tutti i risultati della gara
            nPtot += len(r)
            for p in r:  # per ogni pilota
                if p.position is not None:
                    nP += 1

        return 1 - nP / nPtot


