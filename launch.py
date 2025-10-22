import os
from core import Core,PORT_SERVICE_MAP,CRUD_GATHERINGDB,GenericDAO
from GATHERINGDB.init_db import DatabaseInitializer
from UI.ui import run_ui,GenericModel,UIMapper
class Commands:
    def __init__(self,core:Core=None):
        self.core = core
    def check_db_created(self):
        DatabaseInitializer.check_db_created(self.core,self.core.crud.dao)
    def import_from_nmap_scan(self):
        ip_ports = self.core.parse_greppable_nmap('nmap_scan.gnmap')
        self.core.create_ip_directories(ip_ports,base_dir=os.getcwd())
        self.core.insert_ip_from_nmap(ip_ports=ip_ports)
        # este mismo comando debe de implementar una logica
        # para poder hacer un walk e ingresar dinamicamente a los directorios creados
        # para si el pentester realizo un escaneo entonces ir ahi y re mapear las nuevas direcciones ip
        
def main():
    dao = GenericDAO()
    crud = CRUD_GATHERINGDB(dao)
    core = Core(crud,PORT_SERVICE_MAP)
    cmd = Commands(core)
    generic = GenericModel(repository=core, commands=cmd) 
    generic.cachered_ips
    run_ui(generic)
    cmd.check_db_created()
    cmd.import_from_nmap_scan()

if __name__ == '__main__':
    main()