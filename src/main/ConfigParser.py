import json
from src.main.Ships import Ship, SurfaceShip, Submarine
from src.main.Utility import *
from src.main.NationList import getNationList
from src.main.RefitNode import RefitNode
from typing import Dict, List, Set


class ConfigParser:
    """
    ConfigParser is a decoder/parser that reads serialized game file (generated by 'AL Serializer') and stores them
    It has methods to construct easily usable objects using those game files
    """

    def __init__(self, path: str):
        """
        The constructor of ConfigParser, takes a string and generates a parser object

        :param path: the path to "sharecfg" folder, must be absolute path
        """

        def loadConfig(configName: str) -> Dict:
            configFile = open(path + configName)
            config = json.load(configFile)
            config.pop('all')
            configFile.close()
            return config

        self.shipStatisticDict = loadConfig("ship_data_statistics")
        self.shipDataDict = loadConfig("ship_data_template")
        self.attrDict = loadConfig("attribute_info_by_type")
        self.fleetTechDict = loadConfig("fleet_tech_ship_template")
        self.shipGroupDict = loadConfig("ship_data_group")
        self.shipRefitDict = loadConfig("ship_data_trans")
        self.refitDataDict = loadConfig("transform_data_template")
        self.shipStrengthenDict = loadConfig("ship_data_strengthen")

    def getShip(self, shipID: int) -> Ship:
        """
        Creates a Ship object of the ship that has ID "shipID".
        It will either be a SurfaceShip or a Submarine

        :param shipID: the ID of that ship
        :return: SurfaceShip object or Submarine object depending on its stat
        """
        ID = str(shipID)
        if self.shipStatisticDict[ID]["oxy_max"] == 0:
            return SurfaceShip(self.shipStatisticDict[ID], self.shipDataDict[ID])
        else:
            return Submarine(self.shipStatisticDict[ID], self.shipDataDict[ID])

    def getMetaShip(self, metaId: int):
        """
        Creates MetaShip object from its id metaId

        :param metaId: integer, the in game id of that metaship, usually 1-3 digits
        :return: MetaShip object
        """
        from src.main.MetaShips import MetaShip

        groupId = self.getGroupIdFromMetaId(metaId)
        hasFleetTech = str(groupId) in self.fleetTechDict
        return MetaShip(self.shipGroupDict[str(metaId)], self.shipStrengthenDict[str(groupId)], self, hasFleetTech,
                        fleetTechDict=self.fleetTechDict.get(str(groupId)),
                        refitDict=self.shipRefitDict.get(str(groupId)))

    def getRefitNode(self, refitNodeId: int) -> RefitNode:
        """
        Creates a RefitNode object from its id

        :param refitNodeId: integer, the id of that refit node
        :return: RefitNode object
        """
        reversedAttrDict = self.getReversedAttrDict()
        nodeDict = self.refitDataDict[str(refitNodeId)]
        return RefitNode(nodeDict, reversedAttrDict)

    def getWeapon(self, wepID: int) -> dict:
        pass

    def getSkill(self, skillID: int) -> dict:
        pass

    def getSkillExp(self, skillLevel: int) -> dict:
        pass

    def getAttrDict(self) -> Dict[int, str]:
        """
        This method generates an ship attribute info dict

        :return: An ship attribute info dict which maps attribute ID to it's name (for example FP)
        """
        return {int(ID): x['name'] for ID, x in self.attrDict.items()}

    def getAttrName(self, attrID: int) -> str:
        """
        This method returns an attribute's name based on its ID

        :param attrID: the ID of the attribute, range from 1 to 12
        :return: attribute's name
        """
        return self.getAttrDict()[attrID]

    def getReversedAttrDict(self) -> Dict[str, int]:
        """
        Generates a map from attr name to attr id

        :return: A dict, keys are attr names, values are attr ids
        """
        return {name: ID for ID, name in self.getAttrDict().items()}

    @staticmethod
    def getNation(nationID: int) -> str:
        """
        static method. Returns nation name

        :param nationID: the id of that nation
        :return: nation name
        """
        nationList = getNationList()
        return nationList[nationID]

    def getShipIdList(self) -> Set[int]:
        """
        generates ship id list, automatically filters non-collectable ships

        :return: list of all collectable ship ids
        """
        result = set()
        for _, idList in self.getGroupIdToShipId().items():
            for i in idList:
                result.add(i)
        return result

    def getShipList(self) -> Set[Ship]:
        """
        Generates a set of all unfiltered ships, debug purpose, might be removed in the future

        :return: set of ship objects
        """
        return {self.getShip(ID) for ID in self.getShipIdList()}

    def getShipIdToName(self) -> Dict[int, str]:
        """
        generates a map from shipID to ship's English name

        :return: a dict, keys are ship id (int), values are ship name (string)
        """
        return {ID: (self.shipStatisticDict[str(ID)]['name']
                     + (" BB" if isKagaBB(ID) else "") + " "
                     + "(" + self.shipStatisticDict[str(ID)]['english_name'] + ")") for ID in self.getShipIdList()}

    def getShipNameToId(self) -> Dict[str, int]:
        """
        generates a map from ship's English name to a list of its ship IDs

        :return: a dict, keys are ship name (string), values are a list of ship id (int)
        """
        nameToId = {name: [] for ID, name in self.getShipIdToName().items()}
        for ID, name in self.getShipIdToName().items():
            nameToId[name].append(ID)
        return nameToId

    def getGroupIdList(self) -> Set[int]:
        """
        Generates a set of groupIds of all meta ships

        :return: set of all meta ships' groupId
        """
        return {groupDict["group_type"] for _, groupDict in self.shipGroupDict.items()}

    def getGroupIdToShipId(self) -> Dict[int, List[int]]:
        """
        generates a map from meta ship IDs to ships' ID

        :return: a dict, keys are IDs of meta ship, values are list of ship ids corresponding to that meta ship
        """
        result = {}
        for shipId, groupDict in self.shipDataDict.items():
            shipId = int(shipId)
            metaId = groupDict["group_type"]
            if not isFiltered(shipId):
                if metaId not in result:
                    result[metaId] = []
                result[metaId].append(shipId)
        return result

    def getGroupIdFromMetaId(self, metaId: int) -> Dict[int, int]:
        """
        Returns the corresponding groupId of the meta ship with id metaId

        :param metaId: integer, metaId of that meta ship
        :return: groupId, integer
        """
        for _, data in self.shipGroupDict.items():
            if data["code"] == metaId:
                return data["group_type"]

    def getMetaIdList(self) -> Set[int]:
        """
        Generates a set of meta ship ids

        :return: set of integers, contains ids of all meta ships
        """
        return {int(metaId) for metaId, _ in self.shipGroupDict.items()}
