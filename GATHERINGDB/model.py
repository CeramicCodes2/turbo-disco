from dataclasses import dataclass
import sqlite3
class IntegrityError(Exception):
    def __init__(self, datatype: str, *args):
        super().__init__("Integrity error on table {datatype}".format(datatype=datatype), *args)
        
class TransitiveTable:
    @classmethod
    def create_table(cls) -> str:
        ...

class BaseEntity:

    @classmethod
    def select_map(cls):
        return {}
    @classmethod
    def insert(cls):
        ...
    @classmethod
    def update(cls):
        ...
    @classmethod
    def delete(cls):
        ...
    @classmethod
    def get_guid() -> str:
        # returns an attribute that is the unique identifier of the class
        raise NotImplementedError("Subclasses must implement get_guid method")
    def exportAsTupple(self) -> tuple:
        # returns the attributes of the class as a tupple
        raise NotImplementedError("Subclasses must implement exportAsTupple method")
    @classmethod
    def create_table() -> str:
        # returns the SQL statement to create the table
        raise NotImplementedError("Subclasses must implement create_table method")
    @classmethod
    def select(cls) -> str:
        # returns the SQL statement to select all records from the table
        raise NotImplementedError("Subclasses must implement select method")
    @classmethod
    def selectById(cls) -> str:
        # returns the SQL statement to select a record by its unique identifier
        raise NotImplementedError("Subclasses must implement selectById method")
    @classmethod
    def selectCoincidence(cls) -> str:
        # returns the SQL statement to select records by a field and value
        raise NotImplementedError("Subclasses must implement selectCoincidence method")
@dataclass
class IPNode(BaseEntity):
    id: int
    ip: str
    path:str
    parent_ip: str = None
    child_level:int = 0
    @classmethod
    def get_guid():
        return 'ip'
    @classmethod
    def insert(cls):
        return f"INSERT INTO ip_node(ip,path,parent_ip,child_level) VALUES (?,?,?,?)"
    @classmethod
    def update(cls):
        return f"UPDATE ip_node SET ip=?, path=?, parent_ip=? WHERE ip=?"
    @classmethod
    def delete(cls):
        return f"DELETE FROM ip_node WHERE id=?"
    def exportAsTupple(self):
        return (self.ip,self.path,self.parent_ip,self.child_level)
    @classmethod
    def select(cls):
        
        return "SELECT id, ip, path, parent_ip,child_level FROM ip_node"
    @classmethod
    def selectById(cls):
        return "SELECT id, ip, path, parent_ip FROM ip_node WHERE id=?"
    @classmethod
    def select_map(cls):
        sm = {
            "ip":"SELECT id, ip, path, parent_ip FROM ip_node WHERE  ip = ?",
            "id":"SELECT id, ip, path, parent_ip FROM ip_node WHERE  id = ?",
            "parent_ip":"SELECT id, ip, path, parent_ip FROM ip_node WHERE  parent_ip = ?",
            "child_level":"SELECT id, ip, path, parent_ip FROM ip_node WHERE  child_level = ?",
            "max_child_level_by_parent":"SELECT MAX(child_level) as max_level FROM ip_node where parent_ip = ?"
        }
        return sm
    @classmethod
    def selectCoincidence(cls,field):
        # select map realmente solo son consultas especificas por campo para evitar tener que 
        # crear una consulta que se altere en tiempo de ejecucion que es riesgoso
        sm = cls.select_map().get(field,None)
        if not sm:
            raise ValueError(f"No se definio una consulta de tipo {field} en {cls.__name__} ")
        return sm

    
    @classmethod
    def create_table(cls):
        return '''
            CREATE TABLE IF NOT EXISTS ip_node (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                path TEXT NOT NULL,
                parent_ip TEXT,
                child_level INTEGER DEFAULT 0
            )
        '''
    
        
@dataclass
class Ports(BaseEntity):
    id: int
    port:int
    service_name:str
    ip:str
    @classmethod
    def get_guid():
        return 'port'
    @classmethod
    def insert(cls):
        return f"INSERT INTO ports(port,service_name,ip) VALUES (?,?,?)"
    @classmethod
    def update(cls):
        return f"UPDATE ports SET port=?, service_name=?,ip=? WHERE id=?"
    @classmethod
    def delete(cls):
        return f"DELETE FROM ports WHERE id=?"
    @classmethod
    def select(cls):
        return f"SELECT id, port, service_name, ip FROM ports"
    @classmethod
    def selectById(cls):
        return f"SELECT id, port, service_name, ip FROM ports WHERE id=?"
    @classmethod
    def select_map(cls):
        sm = {
            "ip":"SELECT id, port, service_name,ip parent_ip FROM ports WHERE  ip = ?",
            "id":"SELECT id, port, service_name,ip FROM ports WHERE  id = ?"
        }
        return sm
    @classmethod
    def selectCoincidence(cls,field):
        # select map realmente solo son consultas especificas por campo para evitar tener que 
        # crear una consulta que se altere en tiempo de ejecucion que es riesgoso
        sm = cls.select_map().get(field,None)
        if not sm:
            raise ValueError(f"No se definio una consulta de tipo {field} en {cls.__name__} ")
        return sm
    def exportAsTupple(self):
        return (self.port,self.service_name,self.ip)    
    def create_table():
        return '''
            CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                port INTEGER NOT NULL,
                service_name TEXT NOT NULL,
                ip TEXT NOT NULL,
                FOREIGN KEY(ip) REFERENCES ip_node(ip)
            )
        '''