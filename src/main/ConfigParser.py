import json
from src.main.Ships import Ship, SurfaceShip, Submarine
from src.main.NationList import getNationList
import typing


class ConfigParser:
    def __init__(self, path: str):
        def loadConfig(configName: str):
            configFile = open(path + configName)
            config = json.load(configFile)
            config.pop('all')
            configFile.close()
            return config

        self.shipStatisticDict = loadConfig("ship_data_statistics")
        self.shipDataDict = loadConfig("ship_data_template")
        self.attrDict = loadConfig("attribute_info_by_type")
        self.fleetTechDict = loadConfig("fleet_tech_ship_template")

    def getShip(self, shipID: int) -> Ship:
        ID = str(shipID)
        if self.shipStatisticDict[ID]["oxy_max"] == 0:
            return SurfaceShip(self.shipStatisticDict[ID], self.shipDataDict[ID], self.fleetTechDict[ID[slice(0, -1)]])
        else:
            return Submarine(self.shipStatisticDict[ID], self.shipDataDict[ID], self.fleetTechDict[ID[slice(0, -1)]])

    def getWeapon(self, wepID: int) -> dict:
        pass

    def getSkill(self, skillID: int) -> dict:
        pass

    def getSkillExp(self, skillLevel: int) -> dict:
        pass

    def getAttrDict(self, attrID: int) -> dict:
        return self.attrDict

    def getAttrName(self, attrID: int) -> str:
        return self.attrDict[attrID]

    @staticmethod
    def getNation(nationID: int) -> str:
        nationList = getNationList()
        return nationList[nationID]

    def getShipList(self) -> list:
        return [ID for ID, _ in self.shipStatisticDict.items()]

    def getShipIdToName(self) -> dict:
        return {int(ID): statDict['english_name'] for ID, statDict in self.shipStatisticDict.items()}

    def getShipNameToId(self) -> dict:
        nameToId = {name: [] for ID, name in self.getShipIdToName().items()}
        for ID, name in self.getShipIdToName().items():
            nameToId[name].append(ID)
        return nameToId


