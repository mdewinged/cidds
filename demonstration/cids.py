#!/usr/bin/env python
from functions import *


# Dados 
repository = 'mdewinged/cids'
brint_ip = '192.168.100.100'
int_gateway = '192.168.100.101'
server_subnet = '192.168.100.'
management_subnet = '192.168.200.'
office_subnet = '192.168.210.'
developer_subnet = '192.168.220.'
external_subnet = '192.168.50.'
brex_ip = external_subnet+'100'
ex_gateway= '192.168.50.101'
c1port = 9001
c2port = 9001
nodes = {}


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    unmakeChanges(nodes)
    sys.exit(0)


try:
    # Set up Switches
nodes['brint'] = Switch("brint")
nodes['brint'].instantiate()
nodes['brint'].setIp(brint_ip, 24)
nodes['brint'].connectToInternet(int_gateway, 24)

nodes['brex'] = Switch("brex")
nodes['brex'].instantiate()
nodes['brex'].setIp(brex_ip, 24)
nodes['brex'].connectToInternet(ex_gateway, 24)

# Create Seafile Server
nodes['seafileserver'] = create_node('seafileserver', repository+':seafile', nodes['brex'], external_subnet, 1)
subprocess.run(f'docker cp seafileserver:/home/seafolder seafolder', shell=True)
subprocess.run("cat seafolder", shell=True)
# Change the serverconfig.ini file with the seafilefolder id

# Set up controllers
nodes['c1'] = Controller("c1")
nodes['c1'].instantiate()
nodes['c1'].connect(nodes['brint'])
nodes['c1'].setIp(brint_ip, 24, nodes['brint'])
nodes['c1'].initController(brint_ip, c1port)
nodes['brint'].setController(brint_ip, c1port)

nodes['c2'] = Controller("c2")
nodes['c2'].instantiate()
nodes['c2'].connect(nodes['brex'])
nodes['c2'].setIp(brex_ip, 24, nodes['brex'])
nodes['c2'].initController(brex_ip, c2port)
nodes['brint'].setController(brex_ip, c2port)


# Set Server Subnet
nodes['mail']   = create_node('mailserver',   repository+':mailserver',   nodes['brint'], server_subnet, 1)
nodes['file']   = create_node('fileserver',   repository+':fileserver',   nodes['brint'], server_subnet, 2)
nodes['web']    = create_node('webserver',    repository+':webserver',    nodes['brint'], server_subnet, 3)
nodes['backup'] = create_node('backupserver', repository+':backupserver', nodes['brint'], server_subnet, 4)


# Set Management Subnet
nodes['mprinter'] = create_node('mprinter', repository+'printerserver', nodes['brint'], management_subnet, 1)
nodes['m1'] = create_linuxclient('m1', repository+'linuxclient', nodes['brint'], management_subnet, 2, 'management')
nodes['m2'] = create_linuxclient('m2', repository+'linuxclient', nodes['brint'], management_subnet, 3, 'management')
nodes['m3'] = create_linuxclient('m3', repository+'linuxclient', nodes['brint'], management_subnet, 4, 'management')
nodes['m4'] = create_linuxclient('m4', repository+'linuxclient', nodes['brint'], management_subnet, 5, 'management')
    

# Set Office Subnet
nodes['oprinter'] = create_node('oprinter', repository+'printerserver', nodes['brint'], office_subnet, 1)
nodes['o1'] = create_linuxclient('o1', repository+'linuxclient', nodes['brint'], office_subnet, 2, 'office')
nodes['o2'] = create_linuxclient('o2', repository+'linuxclient', nodes['brint'], office_subnet, 3, 'office')


# Set Developer Subnet
nodes['dprinter'] = create_node('dprinter', repository+'printerserver', nodes['brint'], developer_subnet, 1)
nodes['d1' ] = create_linuxclient('d1',   repository+'linuxclient', nodes['brint'], developer_subnet, 2,  'administrator')
nodes['d2' ] = create_linuxclient('d2',   repository+'linuxclient', nodes['brint'], developer_subnet, 3,  'administrator')
nodes['d3' ] = create_linuxclient('d3',   repository+'linuxclient', nodes['brint'], developer_subnet, 4,  'developer')
nodes['d4' ] = create_linuxclient('d4',   repository+'linuxclient', nodes['brint'], developer_subnet, 5,  'developer')
nodes['d5' ] = create_linuxclient('d5',   repository+'linuxclient', nodes['brint'], developer_subnet, 6,  'developer')
nodes['d6' ] = create_linuxclient('d6',   repository+'linuxclient', nodes['brint'], developer_subnet, 7,  'developer')
nodes['d7' ] = create_linuxclient('d7',   repository+'linuxclient', nodes['brint'], developer_subnet, 8,  'developer')
nodes['d8' ] = create_linuxclient('d8',   repository+'linuxclient', nodes['brint'], developer_subnet, 9,  'developer')
nodes['d9' ] = create_linuxclient('d9',   repository+'linuxclient', nodes['brint'], developer_subnet, 10, 'developer')
nodes['d10'] = create_linuxclient('d10', repository+'linuxclient', nodes['brint'], developer_subnet, 11, 'developer')
nodes['d11'] = create_linuxclient('d11', repository+'linuxclient', nodes['brint'], developer_subnet, 12, 'developer')
nodes['d12'] = create_linuxclient('d12', repository+'linuxclient', nodes['brint'], developer_subnet, 13, 'attacker')
nodes['d13'] = create_linuxclient('d13', repository+'linuxclient', nodes['brint'], developer_subnet, 14, 'attacker')


# Set External Subnet
nodes['eweb'] =  create_node('ewebserver', repository+':webserver',  nodes['brex'], external_subnet, 2)
nodes['e1'] = create_linuxclient('e1', repository+'linuxclient', nodes['brex'], external_subnet, 3, 'external_attacker')
nodes['e2'] = create_linuxclient('e2', repository+'linuxclient', nodes['brex'], external_subnet, 4, 'external_attacker')

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to destroy experiment')
signal.pause()
except Exception as e:
    print(str(e))
    unmakeChanges(nodes)


