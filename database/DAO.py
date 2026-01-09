from database.DB_connect import DBConnect
from model.circuit import Circuit
from model.result import Result


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def defAllDateCampionato():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT s.`year`
                    FROM seasons s 
                    ORDER BY s.`year` DESC"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllCircuiti():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT *
                    FROM circuits c """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append( Circuit(row['circuitId'],
                                row['circuitRef'],
                                row['name'],
                                row['location'],
                                row['country'],
                                row['lat'],
                                row['lng'],
                                row['alt'],
                                row['url'], {})
                       )

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getResByCircuit(anno, circuitId):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT rs.driverId , rs.`position`  
                    FROM races r, results rs, circuits c 
                    WHERE r.raceId = rs.raceId 
                    AND r.circuitId = c.circuitId 
                    AND r.`year` = %s AND c.circuitId = %s"""

        cursor.execute(query, (anno, circuitId))

        res = []
        for row in cursor:
            res.append(Result(row['driverId'],row["position"]))

        cursor.close()
        cnx.close()
        return res


