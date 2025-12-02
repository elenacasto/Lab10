import networkx as nx
from database.dao import DAO
from model.hub import Hub


class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """

        self.G.clear() #svuoto il grafo

        # inserisco i nodi
        self.hubs = {}
        for h in DAO().get_all_hubs():
            hubs = Hub(h["id"], h["codice"], h["nome"], h["citta"], h["stato"],
                       h["latitudine"], h["longitudine"])
            self.hubs[h["id"]] = hubs
            self.G.add_nodes_from(self.hubs)

        #ottengo tutte le tratte A-B
        tratte = DAO().get_tratte()

        #inserisco gli archi
        for t in tratte:
            hub1 = self.hubs[t["hub1"]]
            hub2 = self.hubs[t["hub2"]]

            guadagno_medio = t['valore_totale'] / t['num_spedizioni']

            if guadagno_medio >= threshold:
                self.G.add_edge(hub1, hub2, weight=guadagno_medio)

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """

        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """

        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        result = []
        for u,v,data in self.G.edges(data=True):
            result.append((u, v, data['weight']))
        return result #restituisce tutte le tratte, con il guadagno medio
