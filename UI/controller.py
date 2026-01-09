import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.annoSelezionato1 = None
        self.annoSelezionato2 = None


    def handleBuildGraph(self, e):
        if self.annoSelezionato1 is None or self.annoSelezionato2 is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("Per creare il grafo inserisci un data di inizio e una data di fine"))
            self._view.update_page()
            return
        self._model.creaGrafo(self.annoSelezionato1, self.annoSelezionato2)

        nNodi, nArchi = self._model.getInfoGrafo()
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text("Grafo correttamente creato"))
        self._view._txtGraphDetails.controls.append(ft.Text(f"Il grafo contiene {nNodi} nodi e {nArchi} archi."))

        self._view._btnPrintDetails.disabled = False
        self._view.update_page()


    def handlePrintDetails(self, e):
        res = self._model.componenteConnessaMaggiore()

        self._view._txtGraphDetails.controls.clear()
        for r in res:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{r[0]} -- with score {r[1]}"))

        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        numAnni = int(self._view._txtInNumDiEdizioni.value)
        soglia = int(self._view._txtInSoglia.value)

        listOfCircuits, totScore, listOfScores = self._model.getCampionatoIdeale(soglia, numAnni)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Sotto-campionato ideale composto da {soglia} circuiti in cui si è corso almeno {numAnni} volte:"))
        for c in range(len(listOfCircuits)):
            self._view._txt_result.controls.append(
                ft.Text(f"Circuito {c + 1}: {listOfCircuits[c]} - score: {listOfScores[c]}"))
        self._view._txt_result.controls.append(ft.Text(f"Score totale: {totScore}"))
        self._view.update_page()

    def riempi_ddYear(self):
        anni = self._model.defAllDateCampionato()
        for anno in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(data=anno,
                                                                 text=anno,
                                                                 on_click=self.pickAnnoSelezionato1))
            self._view._ddYear2.options.append(ft.dropdown.Option(data=anno,
                                                                  text=anno,
                                                                  on_click=self.pickAnnoSelezionato2))

    def pickAnnoSelezionato1(self,e):
        self.annoSelezionato1 = e.control.data
        print(self.annoSelezionato1)
        print(type(self.annoSelezionato1))

    def pickAnnoSelezionato2(self,e):
        self.annoSelezionato2 = e.control.data
        print(self.annoSelezionato2)
        print(type(self.annoSelezionato2))


