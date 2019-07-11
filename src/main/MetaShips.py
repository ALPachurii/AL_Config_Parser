import math
from typing import Dict, Union, List, Tuple, Optional
from src.main.ConfigParser import ConfigParser


class MetaShip:
    """
    :param ships:               A map from int (0-3, indicating it's limit break level) to ship object
    :param groupId:             A int, usually 5 digits, sometimes 6 digits, the "group_type" of a meta ship
    :param id:                  A int, usually the in-game id of this ship (for example USS Cassin's id is 005)
                                for research ships their ids are 20000 + in-game id
    """

    def __init__(self, groupDict: Dict[str, Union[int, List]], strengthenDict: Dict[str, Union[int, List[int]]],
                 parser: ConfigParser, hasFleetTech: bool, **kwargs: Dict):
        """
        Constructor of MetaShip class

        :param groupDict: the dict of this meta ship in ship_data_group
        :param parser: the parser that calls this constructor
        :param hasFleetTech: whether this ship has fleet tech stat
        :param kwargs: optional keyword parameter, "refitDict" maps to the refit stat dict, "fleetTechDict" maps to the
                       fleet Tech stat dict
        """
        self.id = groupDict["code"]
        self.groupId = groupDict["group_type"]
        self.hullType = groupDict["type"]
        self.refitHullType = groupDict["trans_type"]
        self.hasRefit = self.refitHullType != 0
        self.refitSkills = groupDict["trans_skill"]
        self.nationality = groupDict["nationality"]

        self.hasFleetTech = hasFleetTech
        if self.hasFleetTech:
            fleetTechDict = kwargs["fleetTechDict"]
            self.fleetTechPoint = [fleetTechDict["pt_get"], fleetTechDict["pt_upgrage"], fleetTechDict["pt_level"]]
            self.fleetStatBonus = [{"attr": fleetTechDict["add_get_attr"], "value": fleetTechDict["add_get_value"]},
                                   {"attr": fleetTechDict["add_level_attr"], "value": fleetTechDict["add_level_value"]}]
        else:
            self.fleetTechPoint = [None, None, None]
            self.fleetStatBonus = [{}, {}]

        self.ships = {}
        self.refitShip = None
        self.changeShipUponRefit = None
        self.changeHullTypeUponRefit = None
        for shipId in parser.getGroupIdToShipId()[self.groupId]:
            if str(self.groupId) in str(shipId):
                suffix = int(str(shipId)[-1])
                self.ships[suffix - 1] = parser.getShip(shipId)
            else:
                self.refitShip = parser.getShip(shipId)
        self.changeShipUponRefit = self.refitShip is not None
        if self.changeShipUponRefit:
            self.changeHullTypeUponRefit = self.hullType != self.refitHullType

        refitNodeCoord = {}  # dict, keys are retrofit node ids, values are coordinates tuple(row, col)
        if self.hasRefit:
            refitDict = kwargs["refitDict"]
            refitList = refitDict["transform_list"]
            zipped = list(zip(refitList, range(1, 7)))
            for colData, col in zipped:
                for nodeData in colData:
                    row = nodeData[0] - 1
                    refitNode = nodeData[1]
                    refitNodeCoord[refitNode] = (row, col)

        self.refitNodeListWithCoord = sorted(
            [(parser.getRefitNode(nodeId), coord) for nodeId, coord in refitNodeCoord.items()],
            key=lambda x: x[0].getId())

        def genStrengthenDict(attrName: str):
            withIndex = zip(range(2, 7), strengthenDict[attrName])
            return {statId: value for statId, value in withIndex}

        self.strengthenValue = genStrengthenDict("durability")
        self.strengthenExpNeeded = genStrengthenDict("level_exp")
        self.strengthenExpProvides = genStrengthenDict("attr_exp")

        self.isResearchShip = self.id > 20000
        self.isCollabShip = 10000 < self.id < 20000

    def getStat(self, statId: int, level: int, lbLevel: int, affBonus: int,
                refitBonus: bool, strengthenBonus: bool) -> int:
        """
        Calculates a stat of this meta ship at certain level, limit break level, affinity, retrofit stat and
        strengthen state.

        :param statId: integer, range from 1 to 12, the id of the stat
        :param level: integer, range from 1 to 120, the level of the ship
        :param lbLevel: integer, range from 0 to 3, the limit break level of the ship
        :param affBonus: integer, range from 0 to 12, the affinity stat bonus of the ship (affBonus%)
        :param refitBonus: boolean, is the ship refitted
        :param strengthenBonus: boolean, is the ship fully strengthened. false means not counting strengthen bonus
        :return:
        """
        if statId < 1 or statId > 12:
            raise ValueError("statId ({}) out of bound".format(statId))
        elif level < 1 or level > 120:
            raise ValueError("level ({}) out of bound".format(level))
        elif lbLevel < 0 or lbLevel > 3:
            raise ValueError("lbLevel ({}) out of bound".format(lbLevel))
        elif affBonus < 0 or affBonus > 12:
            raise ValueError("affBonus ({}) out of bound".format(affBonus))
        else:
            if self.hasRefit and refitBonus and self.changeHullTypeUponRefit:
                baseStat = self.refitShip.getStat(statId, level)
            else:
                baseStat = self.ships[lbLevel].getStat(statId, level)
            strengthenStat = self.strengthenValue.get(statId, 0) if strengthenBonus else 0
            refitStat = sum(map(lambda x: x[0].getStatBonusSum(statId), self.refitNodeListWithCoord)) if refitBonus \
                else 0
            return math.floor((baseStat + strengthenStat) * (1 + affBonus / 100) + refitStat)

    def getEquipProficiency(self, equipSlot: int, lbLevel: int, refitBonus: bool) -> float:
        """
        Calculates the equipment proficiency of a certain slot

        :param equipSlot: integer, range from 1 to 4 the equipment slot, 4 means the fixed weapon on all torpedo ships
        :param lbLevel: integer, range from 0 to 3, the limit break level
        :param refitBonus: boolean, whether count all refit proficiency bonus
        :return: float, the proficiency
        """
        if equipSlot < 1 or equipSlot > 4:
            raise ValueError("equipSlot ({}) out of bound".format(equipSlot))
        elif lbLevel < 0 or lbLevel > 3:
            raise ValueError("lbLevel ({}) out of bound".format(lbLevel))
        elif lbLevel != 3 and refitBonus:
            raise ValueError("Cannot modernize without fully limit break the ship")

        if self.changeHullTypeUponRefit and refitBonus:
            baseProf = self.refitShip.getEquipmentProficiency(equipSlot)
        else:
            baseProf = self.ships[lbLevel].getEquipmentProficiency(equipSlot)

        refitProf = sum([nodeWithCoord[0].getStatBonusSum("equipment_proficiency_{}".format(equipSlot))
                         for nodeWithCoord in self.refitNodeListWithCoord]) if refitBonus else 0
        return refitProf + baseProf

    def getFleetTechPoint(self, stage: int) -> Optional[int]:
        """
        returns the amount of tech points you get from reaching the stage

        :param stage: the stage, 0 means acquiring ship, 1 means mlb-ing, 2 means fully leveling
        :return: tech points, integer
        """
        if stage == 0 or stage == 1 or stage == 2:
            return self.fleetTechPoint[stage]
        else:
            raise ValueError("stage should be 0 - 2")

    def getFleetStatBonus(self, stage: int) -> Tuple[int, int]:
        """
        gets the fleet stat bonus you get from reaching the stage

        :param stage: the stage, integer, 0 means acquiring ship, 1 means fully leveling
        :return: a tuple consist of stat type (integer) and stat value (integer)
        """
        if stage == 0 or stage == 1:
            return self.fleetStatBonus[stage]["attr"], self.fleetStatBonus[stage]["value"]
        else:
            raise ValueError("stage should be 0 or 1")

    pass
