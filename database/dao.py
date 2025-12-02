from database.DB_connect import DBConnect


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_tratte():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT LEAST(s.id_hub_origine, s.id_hub_destinazione) as hub1,
               GREATEST(s.id_hub_origine, s.id_hub_destinazione) as hub2,
               COUNT(*) as num_spedizioni,
               SUM(s.valore_merce) as valore_totale
        FROM spedizione s
        GROUP BY hub1, hub2
        HAVING hub1 <> hub2
        """

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_all_hubs():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * 
        FROM hub
        """

        cursor.execute(query)
        hubs = cursor.fetchall()

        cursor.close()
        conn.close()

        return hubs
