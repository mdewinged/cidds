# Copyright (C) 2022 Alexandre Mitsuru Kaihara
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



import logging
import subprocess
from elements.node import Node


# This class holds the values of the network node link and some
class Link():
    # Brief: Creates Linux virtual interfaces and connects peers to the nodes
    # Params:
    #   String peer1: Reference to the first node object class
    #   String peer2: Reference to the second node object class
    #   String peer1Name: Name of the interface to be connected to the first object
    #   String peer2Name: Name of the interface to be connected to the second object
    # Return:
    #   None
    def __init__(self, peer1: Node, peer2: Node) -> None:
        self.__peer1 = peer1
        self.__peer2 = peer2
        self.__peer1Name = "veth"+self.__peer1.getNodeName()+self.__peer2.getNodeName()
        self.__peer2Name = "veth"+self.__peer2.getNodeName()+self.__peer1.getNodeName()
        self.__connect()

    # Brief: Creates Linux virtual interfaces and connects peers to the nodes
    # Params:
    #   String peer1Ip: Ip of the first peer in format "192.168.56.100"
    #   String peer1Mask: integer corresponding to the subnet mask of peer1 (e.g. 24 = 255.255.0.0)
    #   String peer2Ip: Ip of the second peer in format "192.168.56.100"
    #   String peer2Mask: integer corresponding to the subnet mask of peer2 (e.g. 24 = 255.255.0.0)
    # Return:
    #   None
    def __connect(self) -> None:
        self.__create(self.__peer1Name, self.__peer2Name)
        self.__setInterface(self.__peer1.getNodeName(), self.__peer1Name)
        self.__setInterface(self.__peer2.getNodeName(), self.__peer2Name)

    # Brief: Creates the virtual interfaces and set them up (names cant be the same as some existing one in host's namespace)
    # Params:
    #   String peer1Name: Name of the interface to connect to the first peer 
    #   String peer2Name: Name of the interface to connect to the second peer 
    # Return:
    #   None
    def __create(self, peer1Name: str, peer2Name: str) -> None:
        try:
            subprocess.run(f"ip link add {peer1Name} type veth peer name {peer2Name}", shell=True)
        except Exception as ex:
            logging.error(f"Error while creating virtual interfaces {peer1Name} and {peer2Name}: {str(ex)}")
            raise Exception(f"Error while creating virtual interfaces {peer1Name} and {peer2Name}: {str(ex)}")
    
    # Brief: Set the interface to node
    # Params:
    #   String nodeName: Name of the node network namespace
    #   String peerName: Name of the interface to set to node
    # Return:
    #   None
    def __setInterface(self, nodeName: str, peerName: str) -> None:
        try:
            subprocess.run(f"ip link set {peerName} netns {nodeName}", shell=True)
            subprocess.run(f"ip -n {nodeName} link set {peerName} up", shell=True)
        except Exception as ex:
            logging.error(f"Error while setting virtual interfaces {peerName} to {nodeName}: {str(ex)}")
            raise Exception(f"Error while setting virtual interfaces {peerName} to {nodeName}: {str(ex)}")

    # Brief: Creates a port in OpenvSwitch bridge
    # Params:
    #   String nodeName: The name of the bridge is for default the same name of the switch container
    #   String peerName: Name of the interface to connect to the switch
    # Return:
    #   None
    def __createSwitchPort(self, nodeName, peerName) -> None:
        try:
            subprocess.run(f"docker exec {nodeName} ovs-vsctl add-port {nodeName} {peerName}", shell=True)
        except Exception as ex:
            logging.error(f"Error while creating port {peerName} in switch {nodeName}: {str(ex)}")
            raise Exception(f"Error while creating port {peerName} in switch {nodeName}: {str(ex)}")

    # Brief: Set Ip to an interface (the ip must be set only after connecting it to a container, because)
    # Params:
    #   String nodeName: Name of the node's network namespace
    #   String peerName: Name of the interface to set to node
    #   String ip: IP address to be set to peerName interface
    #   String mask: Network mask for the IP address
    # Return:
    #   None
    def setIp(self, node: Node, ip: str, mask: int) -> None:
        if node == self.__peer1:
            peerName = self.__peer1Name
        elif node == self.__peer2:
            peerName = self.__peer2Name
        else:
            logging.error(f"Incorrect node reference for this Link class, expected reference of object {self.__peer1.getNodeName()} or {self.__peer2.getNodeName()}")
            raise Exception(f"Incorrect node reference for this Link class, expected reference of object {self.__peer1.getNodeName()} or {self.__peer2.getNodeName()}")
            
        if node.__class__.__name__ == "Switch": 
            self.__setSwitchIp(node.getNodeName(), peerName, ip, mask)
            self.__createSwitchPort(node.getNodeName(), peerName)
        else:
            try:
                subprocess.run(f"ip -n {node.getNodeName()} addr add {ip}/{mask} dev {peerName}", shell=True)
            except Exception as ex:
                logging.error(f"Error while setting IP {ip}/{mask} to virtual interface {peerName}: {str(ex)}")
                raise Exception(f"Error while setting IP {ip}/{mask} to virtual interface {peerName}: {str(ex)}")

    # Brief: Set Ip to a bridge 
    # Params:
    #   String nodeName: Name of the node's network namespace
    #   String peerName: Name of the interface to set to node
    #   String ip: IP address to be set to peerName interface
    #   String mask: Network mask for the IP address
    # Return:
    #   None
    def __setSwitchIp(self, nodeName: str, peerName: str, ip: str, mask: int) -> None:
        try:
            subprocess.run(f"ip -n {nodeName} addr add {ip}/{mask} dev {nodeName}", shell=True)
        except Exception as ex:
            logging.error(f"Error while setting IP {ip}/{mask} to virtual interface {peerName}: {str(ex)}")
            raise Exception(f"Error while setting IP {ip}/{mask} to virtual interface {peerName}: {str(ex)}")
    