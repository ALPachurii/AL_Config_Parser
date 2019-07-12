import math
from typing import Dict, Union, List, Tuple, Optional
from .ConfigParser import ConfigParser


class MetaShip:
    """
    :param ships:               A map from int (0-3, indicating it's limit break level) to ship object
    :param groupId:             A int, usually 5 digits, sometimes 6 digits, the "group_type" of a meta ship
    :param id:                  A int, usually the in-game id of this ship (for example USS Cassin's id is 005)
                                for research ships their ids are 20000 + in-game id
    """

    def __init__(self, groupDict: Dict[str, Union[int, List]],
                 parser: ConfigParser, hasFleetTech: bool, **kwargs: Dict):
        """
        Constructor of MetaShip class

        :param groupDict: the dict of this meta ship in ship_data_group
        :param parser: the parser that calls this constructor
        :param hasFleetTech: whether this ship has fleet tech stat
        :param kwargs: optional keyword parameter, "refitDict" maps to the refit stat dict, "fleetTechDict" maps to the
                       fleet Tech stat dict, "researchDict" maps to the research ship data dict
        """
        self.id = groupDict["code"]
        self.groupId = groupDict["group_type"]
        self.hullType = groupDict["type"]
        self.refitHullType = groupDict["trans_type"]
        self.hasRefit = kwargs["refitDict"] is not None
        self.refitSkills = groupDict["trans_skill"]
        self.nationality = groupDict["nationality"]

        self.hasFleetTech = hasFleetTech
        if self.hasFleetTech:
            fleetTechDict = kwargs["fleetTechDict"]
            self.fleetTechPoint = [fleetTechDict["pt_get"], fleetTechDict["pt_upgrage"], fleetTechDict["pt_level"]]
            self.fleetStatBonus = [{fleetTechDict["add_get_attr"]: fleetTechDict["add_get_value"]},
                                   {fleetTechDict["add_level_attr"]: fleetTechDict["add_level_value"]}]
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

        self.isResearchShip = self.id > 20000
        self.isCollabShip = 10000 < self.id < 20000

        self.isSubmarine = self.ships[0].isSubmarine
        self.isSurfaceShip = self.ships[0].isSurfaceShip

        if self.isResearchShip:
            researchDict = kwargs["researchDict"]
            researchEffectIdList = researchDict["strengthen_effect"]
            fateSimIdList = researchDict["fate_strengthen"]
            self.researchNodeList = [parser.getResearchStrengthenNode(nodeId) for nodeId in researchEffectIdList]
            self.fateSimNodeList = [parser.getResearchStrengthenNode(nodeId) for nodeId in fateSimIdList]

    def getLocalizedName(self) -> str:
        """
        Gets the localized name (uncensored)

        :return: string, name
        """
        return self.ships[0].name

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
            # bulin compatibility
            if self.id in [1, 2]:
                lbLevel = 0

            if self.hasRefit and refitBonus and self.changeShipUponRefit:
                baseStat = self.refitShip.getStat(statId, level, strengthenBonus)
            else:
                baseStat = self.ships[lbLevel].getStat(statId, level, strengthenBonus)

            refitStat = sum(map(lambda x: x[0].getStatBonusSum(statId), self.refitNodeListWithCoord)) if refitBonus \
                else 0
            researchStrengthenStat = sum([researchNode.getStatBonus(statId) for researchNode in self.researchNodeList])\
                if (self.isResearchShip and strengthenBonus) else 0
            return math.floor((baseStat + researchStrengthenStat) * (1 + affBonus / 100) + refitStat)

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

        if self.changeShipUponRefit and refitBonus:
            baseProf = self.refitShip.getEquipmentProficiency(equipSlot)
        else:
            baseProf = self.ships[lbLevel].getEquipmentProficiency(equipSlot)

        refitProf = sum([nodeWithCoord[0].getStatBonusSum("equipment_proficiency_{}".format(equipSlot))
                         for nodeWithCoord in self.refitNodeListWithCoord]) if refitBonus else 0
        return refitProf + baseProf

    def getEquipBaseCount(self, equipSlot: int, lbLevel: int, isRefitted: bool) -> int:
        """
        Gets the base count of a certain equipment slot

        :param equipSlot: integer, range from 1 to 3, the slot number
        :param lbLevel: integer, range from 0 to 3, the limit break level
        :param isRefitted: boolean
        :return: integer, the base count
        """
        if equipSlot < 1 or equipSlot > 3:
            raise ValueError("equipSlot ({}) out of bound".format(equipSlot))
        elif lbLevel < 0 or lbLevel > 3:
            raise ValueError("lbLevel ({}) out of bound".format(lbLevel))
        elif lbLevel != 3 and isRefitted:
            raise ValueError("Cannot modernize without fully limit break the ship")

        if self.changeShipUponRefit and isRefitted:
            return self.refitShip.getEquipBase(equipSlot)
        else:
            return self.ships[lbLevel].getEquipBase(equipSlot)

    def getEquipType(self, equipSlot: int, lbLevel: int, isRefitted: bool) -> List[int]:
        """
        Gets a list of allowed equipment type of a certain equipment slot

        :param equipSlot: integer, range from 1 to 5, the slot number (1 is the first slot)
        :param lbLevel: integer, range from 0 to 3, the limit break level
        :param isRefitted: boolean
        :return: List of integers, a list containing all allowed equipment type
        """
        if equipSlot < 1 or equipSlot > 5:
            raise ValueError("equipSlot ({}) out of bound".format(equipSlot))
        elif lbLevel < 0 or lbLevel > 3:
            raise ValueError("lbLevel ({}) out of bound".format(lbLevel))
        elif lbLevel != 3 and isRefitted:
            raise ValueError("Cannot modernize without fully limit break the ship")

        if self.changeShipUponRefit and isRefitted:
            return self.refitShip.getEquipmentType(equipSlot)
        else:
            return self.ships[lbLevel].getEquipmentType(equipSlot)

    def getFleetTechPoint(self, stage: int) -> Optional[int]:
        """
        returns the amount of tech points you get from reaching the stage

        :param stage: the stage, 0 means acquiring ship, 1 means mlb-ing, 2 means fully leveling
        :return: tech points, None means no fleet tech points
        """
        if stage in [0, 1, 2]:
            return self.fleetTechPoint[stage]
        else:
            raise ValueError("stage should be 0 - 2")

    def getFleetStatBonus(self, stage: int) -> Tuple[Optional[int], Optional[int]]:
        """
        gets the fleet stat bonus you get from reaching the stage

        :param stage: the stage, integer, 0 means acquiring ship, 1 means fully leveling
        :return: a tuple consist of stat type (integer or None) and stat value (integer or None)
        """
        if stage in [0, 1]:
            if len(self.fleetStatBonus[stage]) == 0:
                return None, None
            for statId, value in self.fleetStatBonus[stage].items():
                return statId, value
        else:
            raise ValueError("stage should be 0 or 1")

    def getAmmo(self) -> int:
        if self.isSubmarine:
            return self.ships[0].getAmmo()
        else:
            raise NotImplementedError("getAmmo method for surface ships")

    def getOxygen(self, lbLevel: int) -> int:
        if self.isSubmarine:
            return self.ships[lbLevel].getOxygen()
        else:
            raise NotImplementedError("getOxygen method for surface ships")

    def getHuntingRange(self, lbLevel: int) -> List[List[List[int]]]:
        if self.isSubmarine:
            return self.ships[lbLevel].getHuntingRange()
        else:
            raise NotImplementedError("getHuntingRange method for surface ships")

    pass
