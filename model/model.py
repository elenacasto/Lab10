import networkx as nx
from database.dao import DAO


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

        #ottengo tutte le tratte A-B
        tratte = DAO().get_tratte()

        #inserisco i nodi
        for t in tratte:
            hub1 = (t.hub1.id, t.hub1.nome)
            hub2 = (t.hub2.id, t.hub2.nome)

            self.G.add_node(hub1[0], nome=hub1[1])
            self.G.add_node(hub2[0], nome=hub2[1])

        #inserisco gli archi
        for t in tratte:
            guadagno_medio = t['valore_totale'] / t['num_spedizioni']

            if guadagno_medio >= threshold:
                self.G.add_node(t['hub1_id'], nome=t['hub1_nome'], stato=t['hub1_stato'])
                self.G.add_node(t['hub2_id'], nome=t['hub2_nome'], stato=t['hub2_stato'])

                self.G.add_edge(
                    t['hub1_id'], t['hub2_id'],
                    weight=guadagno_medio,
                    num_spedizioni=t['num_spedizioni'],
                    valore_totale=t['valore_totale'],
                    hub1_nome=t['hub1_nome'],
                    hub1_stato=t['hub1_stato'],
                    hub2_nome=t['hub2_nome'],
                    hub2_stato=t['hub2_stato']
                )

        return self.G

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

        return list(self.G.edges(data=True)) #restituisce tutte le tratte, con i dati inseriti in precedenza
