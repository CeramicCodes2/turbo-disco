import unittest
from unittest.mock import MagicMock
from GATHERINGDB.model import IPNode, Ports
from GATHERINGDB.dao import GenericDAO
from your_module import CRUD_GATHERINGDB  # Ajusta el import según tu estructura

class TestCRUD_GATHERINGDB(unittest.TestCase):
    def setUp(self):
        self.mock_dao = MagicMock(spec=GenericDAO)
        self.crud = CRUD_GATHERINGDB(dao=self.mock_dao)

    def test_select_ip_by_field_success(self):
        self.mock_dao.seleccionarCoincidencia.return_value = [IPNode(id=1, ip='192.168.1.1', parent_ip='', path='/')]
        result = self.crud.select_ip_by_field('ip', '192.168.1.1', dao=self.mock_dao)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ip, '192.168.1.1')

    def test_select_ip_by_field_failure(self):
        self.mock_dao.seleccionarCoincidencia.side_effect = Exception("DB error")
        result = self.crud.select_ip_by_field('ip', '192.168.1.1', dao=self.mock_dao)
        self.assertEqual(result, [])

    def test_insert_port_node_success(self):
        ipnode = IPNode(id=1, ip='192.168.1.1', parent_ip='', path='/')
        self.mock_dao.seleccionarPorId.return_value = ipnode
        self.crud.insert_port_node(1, 8080, dao=self.mock_dao)
        self.mock_dao.insertar.assert_called_once()
        args = self.mock_dao.insertar.call_args[0][0]
        self.assertIsInstance(args, Ports)
        self.assertEqual(args.port, 8080)

    def test_insert_port_node_invalid_ip(self):
        self.mock_dao.seleccionarPorId.return_value = None
        with self.assertLogs('GATHERINGDB.log', level='ERROR'):
            self.crud.insert_port_node(99, 8080, dao=self.mock_dao)

    def test_insert_ip(self):
        self.crud.insert_ip('192.168.1.2', '/path', '192.168.1.1', dao=self.mock_dao)
        self.mock_dao.insertar.assert_called_once()
        ipnode = self.mock_dao.insertar.call_args[0][0]
        self.assertEqual(ipnode.ip, '192.168.1.2')

    def test_show_all_data(self):
        self.mock_dao.seleccionar.return_value = [IPNode(id=1, ip='192.168.1.1', parent_ip='', path='/')]
        count = self.crud.show_all_data(IPNode, dao=self.mock_dao)
        self.assertEqual(count, 1)

    def test_select(self):
        self.mock_dao.seleccionar.return_value = [IPNode(id=1, ip='192.168.1.1', parent_ip='', path='/')]
        result = self.crud.select(IPNode, dao=self.mock_dao)
        self.assertEqual(len(result), 1)

    def test_delete_ip_success(self):
        ipnode = IPNode(id=1, ip='192.168.1.1', parent_ip='', path='/')
        self.mock_dao.seleccionarPorId.return_value = ipnode
        self.crud.delete_ip(1, dao=self.mock_dao)
        self.mock_dao.eliminar.assert_called_once_with(ipnode, 1)

    def test_delete_ip_not_found(self):
        self.mock_dao.seleccionarPorId.return_value = None
        with self.assertLogs('GATHERINGDB.log', level='ERROR'):
            self.crud.delete_ip(99, dao=self.mock_dao)

    def test_update_ip_success(self):
        ipnode = IPNode(id=1, ip='192.168.1.1', parent_ip='', path='/')
        self.mock_dao.seleccionarPorId.return_value = ipnode
        self.crud.update_ip(1, ipnode, dao=self.mock_dao)
        self.mock_dao.actualizar.assert_called_once_with(ipnode, 1)

    def test_update_ip_not_found(self):
        self.mock_dao.seleccionarPorId.return_value = None
        with self.assertLogs('GATHERINGDB.log', level='ERROR'):
            self.crud.update_ip(99, IPNode(id=99, ip='192.168.1.99', parent_ip='', path='/'), dao=self.mock_dao)

if __name__ == '__main__':
    unittest.main()
