from src.main.Ships import Ship, SurfaceShip, Submarine
from typing import List


class MetaShip(Ship):
    """
    MetaShip is an abstraction of all of its subships, its stats are the same as mlb version of its subship
    """

    def __init__(self, statDict: dict, dataDict: dict, fleetTechStat: dict):
        Ship.__init__(self, statDict, dataDict, fleetTechStat)
        self.id = int(str(self.id)[slice(0, -1)])


class MetaSurfaceShip(MetaShip):
    def __init__(self, statDict: dict, dataDict: dict, fleetTechStat: dict):
        MetaShip.__init__(self, statDict, dataDict, fleetTechStat)
        self.isSubmarine = False
        self.isSurfaceShip = True

    def isSubmarine(self) -> bool:
        """
        check if this ship is submarine
        :return: true if this is a submarine otherwise false
        """
        return self.isSubmarine

    def isSurfaceShip(self) -> bool:
        """
        check if this ship is surface ship
        :return: true if this is a surface ship otherwise false
        """
        return self.isSurfaceShip


class MetaSubmarine(MetaShip):
    def __init__(self, statDict: dict, dataDict: dict, fleetTechStat: dict):
        MetaShip.__init__(self, statDict, dataDict, fleetTechStat)
        self.isSubmarine = True
        self.isSurfaceShip = False
        self.oxygen = statDict["oxy_max"]
        self.oxyCost = statDict["oxy_cost"]
        self.oxyRecovery = statDict["oxy_recovery"]
        self.ammo = statDict["ammo"]
        self.surfaceDuration = statDict["attack_duration"]
        self.huntingRangeLevel = statDict["huntingrange_level"]
        self.huntingRange = statDict["hunting_range"]

    def isSubmarine(self) -> bool:
        """
        check if this ship is submarine
        :return: true if this is a submarine otherwise false
        """
        return self.isSubmarine

    def isSurfaceShip(self) -> bool:
        """
        check if this ship is surface ship
        :return: true if this is a surface ship otherwise false
        """
        return self.isSurfaceShip

    def getOxygen(self) -> int:
        """
        get the maximum oxygen of this ship
        :return: oxygen, integer
        """
        return self.oxygen

    def getOxyCost(self) -> int:
        """
        get the oxygen cost per second of this ship
        :return: oxygen consumption speed, integer
        """
        return self.oxyCost

    def getAmmo(self) -> int:
        """
        get the ammo count of this ship
        :return: ammo count, integer
        """
        return self.ammo

    def getHuntingRange(self) -> List[List[List[int]]]:
        """
        get the hunting range of this ship
        :return: hunting range, list of lists of lists of integers
        """
        return self.huntingRange

    def getHuntingRangeLevel(self) -> int:
        """
        get the hunting range level of this ship
        :return: hunting range level, integer
        """
        return self.huntingRangeLevel
