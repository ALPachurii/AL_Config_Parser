from typing import Dict, Union, List, Tuple, Optional
from src.main.ConfigParser import ConfigParser


class MetaShip:
    """
    Attributes:
        ships               A map from int (0-3, indicating it's limit break level) to ship object
        groupId             A int, usually 5 digits, sometimes 6 digits, the "group_type" of a meta ship
        id                  A int, usually the in-game id of this ship (for example USS Cassin's id is 005)
                            for research ships their ids are 20000 + in-game id
    """
    def __init__(self, groupDict: Dict[str, Union[int, List]], parser: ConfigParser, hasFleetTech: bool, *args: Dict):
        self.id = groupDict["code"]
        self.groupId = groupDict["group_type"]
        self.hullType = groupDict["type"]
        self.refitHullType = groupDict["trans_type"]
        self.hasRefit = self.refitHullType != 0
        self.refitSkills = groupDict["trans_skill"]
        self.nationality = groupDict["nationality"]

        self.hasFleetTech = hasFleetTech
        if self.hasFleetTech:
            fleetTechDict = args[0]
            self.fleetTechPoint = [fleetTechDict["pt_get"], fleetTechDict["pt_upgrage"], fleetTechDict["pt_level"]]
            self.fleetStatBonus = [{"attr": fleetTechDict["add_get_attr"], "value": fleetTechDict["add_get_value"]},
                                   {"attr": fleetTechDict["add_level_attr"], "value": fleetTechDict["add_level_value"]}]
        else:
            self.fleetTechPoint = [None, None, None]
            self.fleetStatBonus = [{}, {}]

        self.ships = {}
        self.refitShip = None
        for shipId in parser.getGroupIdToShipId()[self.groupId]:
            if str(self.groupId) in str(shipId):
                suffix = int(str(shipId)[-1])
                self.ships[suffix - 1] = parser.getShip(shipId)
            else:
                self.refitShip = parser.getShip(shipId)
        self.changeShipUponRefit = self.refitShip is not None
        self.changeHullTypeUponRefit = self.hullType == self.refitHullType

        refitNodeWithCoord = {}  # dict, keys are retrofit node ids, values are coordinates tuple(row, col)
        if self.hasRefit:
            refitDict = args[1]
            refitList = refitDict["transform_list"]
            zipped = list(zip(refitList, range(1, 7)))
            for i in zipped:
                colData, col = i
                for nodeData in colData:
                    row = nodeData[0] - 1
                    refitNode = nodeData[1]
                    refitNodeWithCoord[refitNode] = (row, col)

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
        get the fleet stat bonus you get from reaching the stage
        :param stage: the stage, integer, 0 means acquiring ship, 1 means fully leveling
        :return: a tuple consist of stat type (integer) and stat value (integer)
        """
        if stage == 0 or stage == 1:
            return self.fleetStatBonus[stage]["attr"], self.fleetStatBonus[stage]["value"]
        else:
            raise ValueError("stage should be 0 or 1")

    pass
