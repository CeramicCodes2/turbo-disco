import os
from GATHERINGDB.dao import GenericDAO,Transaction
from GATHERINGDB.model import IPNode,Ports
from GATHERINGDB.init_db import DatabaseInitializer
from GATHERINGDB.log import log



class CRUD_GATHERINGDB:
    def __init__(self, dao:GenericDAO=None):
        self.dao = dao       
    def insert_port_node(self,ip_id,ports,dao:GenericDAO=None):
        try:
            data =dao.seleccionarPorId(IPNode,ip_id)
            if not data:
                raise ValueError(f"No IPNode found with id {ip_id}")
            ports = Ports(id=0,port=ports,service_name='unknown',ip=data.ip)
            dao.insertar(ports)
        except Exception as e:
            print(f"[-] error inserting node \n {e}")
    def insert_ip(self,ip:str,current_path:str,parent_ip:str, dao:GenericDAO=None):
        node = IPNode(id=0,ip=ip, parent_ip=parent_ip,path=current_path)
        dao.insertar(node)
    def show_all_data(self,data,dao:GenericDAO=None):
        nodes = dao.seleccionar(data)
        for node in nodes:
            print(node)
    def delete_ip(self,ip_id:int,dao:GenericDAO=None):
        try:
            data =dao.seleccionarPorId(IPNode,ip_id)
            if not data:
                raise ValueError(f"No IPNode found with id {ip_id}")
            dao.eliminar(data,data.id)
        except Exception as e:
            print(f"[-] error deleting node \n {e}")
    def update_ip(self,ip_id:int,new_ip:str,new_path:str,dao:GenericDAO=None):
        try:
            data =dao.seleccionarPorId(IPNode,ip_id)
            if not data:
                raise ValueError(f"No IPNode found with id {ip_id}")
            data.ip = new_ip
            data.path = new_path
            dao.actualizar(data)
        except Exception as e:
            print(f"[-] error updating node \n {e}")


def main():
    dao = GenericDAO()
    crud = CRUD_GATHERINGDB(dao)
    crud.show_all_data(IPNode,dao=dao)
    crud.show_all_data(Ports,dao=dao)
    #crud.insert_ip('192.168.2.1',os.getcwd(),'', dao=dao)
    #crud.insert_ip('192.168.2.5',os.getcwd(),'', dao=dao)
    #crud.insert_port_node(1, 8080, dao=dao)
    crud.delete_ip(1, dao=dao)

if __name__ == '__main__':
    DatabaseInitializer.initialize_db(dao=GenericDAO())
    
    main()
# posible feature
# agregar un generador de nombres aleatorios para las direcciones IP y estos nombres pasarlos
# a una funcion que genere vareables de entorno para que se pueda facilmente se;alar la direccion IP 

    