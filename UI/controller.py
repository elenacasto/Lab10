import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """

        #mi assicuro che il valore inserito sia valido
        guadagno_str = self._view.guadagno_medio_minimo.value
        try:
            guadagno = float(guadagno_str)
        except ValueError:
            self._view.show_alert("Inserire un numero valido!")
            return

        self._model.costruisci_grafo(guadagno)

        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()
        tratte = self._model.get_all_edges()

        #aggiorno la listview
        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Hubs: {num_nodi}")
        )

        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Tratte: {num_archi}")
        )

        for i, (u, v, valore) in enumerate(tratte, start=1):
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{i}) [{u.nome}({u.stato}) -> {v.nome}({v.stato})] -- "
                 f"guadagno Medio Per Spedizione: {valore:.2f}€")
            )

        self._view.update()