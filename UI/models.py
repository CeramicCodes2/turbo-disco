#from . import IPNode
from collections import defaultdict

class RepositoryModel:
    def __init__(self, repository):
        # repository can be a callable/class or an instance
        self.repository = repository() if callable(repository) else repository


class CommandModel:
    def __init__(self, commands):
        self.commands = commands


class UIMapper:
    """Convierte entidades IPNode y Ports en una lista de tuplas
    (ip_str, parent_ip_str, [protocols...]) para uso en la UI.

    Se puede inicializar vacío y luego cargar datos con `from_core` o
    pasando listas de entidades con `load(ips, ports)`.
    """
    def __init__(self, port_service_map: dict = None):
        self.port_service_map = port_service_map or {}
        self._value = []

    def load(self, ips, ports):
        """Construye la representación UI a partir de listas de entidades.

        ips: iterable de objetos IPNode (deben tener atributos .ip, .parent_ip y opcional .id)
        ports: iterable de objetos Port (deben tener atributos .port, .service_name y referencia a ip: .ip o .ip_id)
        """
        
        # mapas auxiliares
        ip_by_id = {}
        ip_by_ip = {}
        for ip in ips or []:
            if hasattr(ip, 'id'):
                ip_by_id[getattr(ip, 'id')] = ip
            ip_by_ip[getattr(ip, 'ip', None)] = ip

        protocols_by_ip = defaultdict(list)

        for p in ports or []:
            # resolver la entidad IP asociada al puerto
            ip_entity = None
            # varios posibles campos: ip (string), ip (int id), ip_id
            if hasattr(p, 'ip'):
                val = getattr(p, 'ip')
                ip_entity = ip_by_ip.get(val)

            if not ip_entity:
                # no podemos mapear este puerto a una IP conocida
                continue

            # determinar nombre del servicio/protocolo
            service = getattr(p, 'service_name', None)
            if not service:
                portnum = getattr(p, 'port', None)
                service = self.port_service_map.get(portnum, f'port_{portnum}')
            if ip_entity.ip:
                protocols_by_ip[ip_entity.ip].append(service)

        # construir la lista final
        result = []
        for ip in ips or []:
            ip_str = getattr(ip, 'ip', None)
            parent = getattr(ip, 'parent_ip', None)
            path = getattr(ip, 'path', '')
            # fallback: algunos modelos usan 'path' para la carpeta
            if parent is None:
                parent = ''
                # path = getattr(ip, 'path', None)
                
            protocols = protocols_by_ip.get(ip_str, [])
            result.append((ip_str, parent, protocols))#,path))

        self._value = result

    def from_core(self, core):
        """Cargar datos desde una instancia `core` que expone
        `select_all_ips()` y `select_all_ports()`.
        """
        ips = core.select_all_ips()
        ports = core.select_all_ports()
        print(ips,ports)
        self.load(ips, ports)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, data):
        # si se recibe una tupla/lista de (ips, ports)
        if isinstance(data, tuple) and len(data) == 2:
            self.load(data[0], data[1])
        else:
            # si se recibe una lista ya transformada
            self._value = data


class GenericModel:
    def __init__(self, repository, commands=None, port_service_map=None):
        self.repo = RepositoryModel(repository)
        self.cmd = CommandModel(commands)
        self.mapper = UIMapper(port_service_map=port_service_map)
        self._cachered = []
        self.protocols = ["SMB", "FTP", "SSH", "HTTP", "DNS", "RDP", "Telnet", "SMTP", "POP3", "IMAP", "LDAP", "SNMP"]

    @property
    def cachered_ips(self):
        if not self._cachered:
            ips = None
            ports = None
            repo = self.repo.repository
            # repository puede exponer select_all_ips/select_all_ports
            if hasattr(repo, 'select_all_ips'):
                ips = repo.select_all_ips()
            if hasattr(repo, 'select_all_ports'):
                ports = repo.select_all_ports()

            # si no hay ports disponibles pero el repo es en realidad un Core


            # cargar en el mapper
            self.mapper.load(ips or [], ports or [])
            self._cachered = self.mapper.value
        return self._cachered
    # es necesario crear un modelo
    # muy similar al que maneja la intefaz