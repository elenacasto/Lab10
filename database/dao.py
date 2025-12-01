from database.DB_connect import DBConnect
from model.hub import Hub
from model.spedizione import Spedizione


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    def __init__(self):
        pass

    @staticmethod
    def get_tratte():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT h1.id as hub1_id,
               h2.id as hub2_id,
               h1.nome as hub1_nome,
               h2.nome as hub2_nome,
               h1.stato as hub1_stato, h2.stato as hub2_stato,
               COUNT(*) as num_spedizioni,
               SUM(valore_merce) as valore_totale
        FROM spedizione s, hub h1, hub h2
        WHERE h1.id = LEAST(s.id_hub_origine, s.id_hub_destinazione)
              AND h2.id = GREATEST(s.id_hub_origine, s.id_hub_destinazione)
        GROUP BY hub1_id, hub2_id, hub1_nome, hub2_nome, hub1_stato, hub2_stato
        ORDER BY hub1_id, hub2_id
        """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

    def get_all(self):
        pass
