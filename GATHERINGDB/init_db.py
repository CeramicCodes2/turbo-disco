from GATHERINGDB.dao import GenericDAO,Transaction
from GATHERINGDB.model import IPNode,Ports
class DatabaseInitializer:
    ''' Clase para inicializar la base de datos '''
    @classmethod
    def initialize_db(cls,dao:GenericDAO=None):
        # crear la tabla si no existe
        with dao.conn() as connection:
            with Transaction(connection,dao.conn) as cursor:
                cursor.execute(IPNode.create_table())
                cursor.execute(Ports.create_table())