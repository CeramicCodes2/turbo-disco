from GATHERINGDB.main import CRUD_GATHERINGDB,GenericDAO
from collections import defaultdict
import re
import os
PORT_SERVICE_MAP = {
    21: 'ftp',
    22: 'ssh',
    3389: 'rdp',
    80: 'http',
    443: 'https',
    139: 'smb',
    445: 'smb',
    3306: 'mysql',
    5432: 'postgres',
    25: 'smtp',
    110: 'pop3',
    143: 'imap'
}


class Core:
    def __init__(self,crud:CRUD_GATHERINGDB=None,PORT_SERVICE_MAP:dict[int,str]=None):
        self.crud = crud
        self.port_service_map = PORT_SERVICE_MAP
    def insert_ip_from_directory(self,current_path, parent_ip=None):
        for entry in os.listdir(current_path):
            ip = re.search(r'\s+([\d\.]+)', entry).group(1)
            if not(ip):
                continue # not founded any ip !
            full_path = os.path.join(current_path, entry)
            
            if os.path.isdir(full_path):
                self.crud.insert_ip(entry,full_path,None, dao=self.crud.dao)
                self.insert_ip_from_directory(full_path, entry)
    def insert_services_from_directory(self,current_path, ip):
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                service_name = entry
                port = None
                for p, s in self.port_service_map.items():
                    if s == service_name:
                        port = p
                        break
                if port:
                    self.crud.insert_port_node(ip, port, dao=self.crud.dao)
                self.insert_services_from_directory(full_path, ip)
    def insert_ip_from_nmap(self,ip_ports):
        for ip, ports in ip_ports.items():
            self.crud.insert_ip(ip, os.getcwd(), '', dao=self.crud.dao)
            for port in ports:
                self.crud.insert_port_node(ip, port, dao=self.crud.dao)
    def parse_greppable_nmap(self,file_path):
        ip_ports = defaultdict(list)

        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('Host:'):
                    match_ip = re.search(r'Host:\s+([\d\.]+)', line)
                    match_ports = re.findall(r'(\d+)/open', line)

                    if match_ip:
                        ip = match_ip.group(1)
                        ports = [int(p) for p in match_ports]
                        ip_ports[ip].extend(ports)

        return ip_ports
    def create_ip_directories(self,ip_ports, base_dir='scan_results'):
        os.makedirs(base_dir, exist_ok=True)

        for ip, ports in ip_ports.items():
            ip_dir = os.path.join(base_dir, ip)
            os.makedirs(ip_dir, exist_ok=True)

            for port in ports:
                service = self.port_service_map.get(port, f'port_{port}')
                service_dir = os.path.join(ip_dir, service)
                os.makedirs(service_dir, exist_ok=True)
def main():
    dao = GenericDAO()
    crud = CRUD_GATHERINGDB(dao)
    core = Core(crud,PORT_SERVICE_MAP)
    core.insert_ip_from_directory(os.getcwd())
    ip_ports = core.parse_greppable_nmap('nmap_scan.gnmap')

if __name__ == '__main__':
    main()