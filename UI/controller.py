import flet as ft
from UI.view import View
from database.dao import DAO
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
        # TODO

        #mi assicuro che il valore inserito sia valido
        guadagno_str = self._view.guadagno_medio_minimo.value
        try:
            guadagno = float(guadagno_str)
        except ValueError:
            self._view.show_alert("Inserire un numero valido!")
            return

        tratte = DAO().get_tratte()
        self._model.G.clear()

        for t in tratte:
            hub1 = t["hub1_id"]
            hub2 = t["hub2_id"]
            valore_totale = t["valore_totale"]
            num_spedizioni = t["num_spedizioni"]

            guadagno_medio = valore_totale / num_spedizioni

            if guadagno_medio >= guadagno:
                self._model.G.add_node(hub1)
                self._model.G.add_node(hub2)
                self._model.G.add_edge(hub1, hub2,
                                       weight= guadagno_medio,
                                       num_spedizioni= num_spedizioni,
                                       valore_totale = valore_totale,
                                       hub1_nome=t.hub1.nome,
                                       hub2_nome=t.hub2.nome,
                                       hub1_stato=t.hub1.stato,
                                       hub2_stato=t.hub2.stato
                                       )
        #aggiorno la listview
        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Hubs: {self._model.get_num_nodes()}")
        )

        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Tratte: {self._model.get_num_edges()}")
        )

        for i, (u, v, data) in enumerate(self._model.get_all_edges()):
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{i + 1}) [{data['hub1_nome']}({data['hub1_stato']}) -> "
                     f"{data['hub2_nome']}({data['hub2_stato']})] -- "
                     f"guadagno Medio Per Spedizione: € {data['weight']:.2f}")

            )

        self._view.update()