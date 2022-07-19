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


from node import Node


# Brief: This class defines the metaclass of Topology in order to implement Singleton Pattern
class TopologyMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
        

# Brief: This class is responsible to store all the informations of all nodes
class Topology(metaclass=TopologyMeta):
    def __init__(self):
        self.__nodes = {}

    def setNode(self, node: Node) -> None:
        self.__nodes[node.getNodeName()] = {}
        self.__nodes[node.getNodeName()]["nodeRef"] = node
        self.__nodes[node.getNodeName()]["connections"] = {}
        self.__nodes[node.getNodeName()]["ip"] = []
        self.__nodes[node.getNodeName()]["gateway"] = 0
    
    # Brief: Save the ip and mask information
    # Params:
    #   String ip: IP address to be set to peerName interface
    #   int mask: Integer that represents the network mask
    #   String interfaceName: The name of the interface the IP was set
    # Return:
    #   None
    def setNodeIp(self, node: Node, ip: str, mask: int, interfaceName: str) -> None:
        self.__ipv4[node.getNodeName()]["ip"].append({ip, mask, interfaceName})

    # Brief: Returns the container network informations 
    # Params:
    #   Node node: Refernce to the node to get the container informations
    # Return:
    def getNode(self, node: Node) -> None:
        return self.__nodes[node.getNodeName()]

    # Brief: Check if this container is connected to another node reference
    # Params:
    #   Node node: Reference to the node to check if this container is connected to
    # Return:
    #   None
    def isConnected(self, node: Node, destNode: Node) -> None:
        # Check if the received node is already connected to this container
        try:
            self.__connections[node.getNodeName()]
        except:
            logging.error(f"Incorrect node reference for {self.getNodeName()}, connect {destNode.getNodeName()} first")
            raise Exception(f"Incorrect node reference for {self.getNodeName()}, connect {destNode.getNodeName()} first")
