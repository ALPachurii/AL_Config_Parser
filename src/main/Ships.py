from typing import List, Tuple
from src.main.Utility import isKagaBB


class Ship:
    """
    Supertype of SurfaceShip and Submarine. Ship class stores all info of a ship and has methods to access them.
    """

    def __init__(self, statDict: dict, dataDict: dict):
        self.id = statDict["id"]
        self.name = statDict["name"]
        self.englishName = statDict["english_name"]
        self.attrs = statDict["attrs"]
        self.rarity = statDict["rarity"]
        self.star = statDict["star"]
        self.proficiency = statDict["equipment_proficiency"]
        self.attrsGrowth = statDict["attrs_growth"]
        self.attrsGrowthExtra = statDict["attrs_growth_extra"]
        self.hullType = statDict["type"]

        self.defaultDepthChargeList = statDict["depth_charge_list"]
        self.defaultEquipList = statDict[
            "default_equip_list"]  # default equipment(when you don't equip equipments) list
        self.equipPreloadList = statDict["preload_count"]  # equipment preload list
        self.fixedEquipList = statDict["fix_equip_list"]  # "magic cannon"
        self.equipBaseList = statDict["base_list"]  # equipment base count list
        self.equipTypeList = [dataDict["equip_1"], dataDict["equip_2"], dataDict["equip_3"], dataDict["equip_4"],
                              dataDict["equip_5"]]

        self.skillList = dataDict["buff_list_display"]

    def getStat(self, statID: int, level: int) -> float:
        """
        calculates ship's base stat at certain level

        :param statID: id of that attribute/stat
        :param level: the level, range from 1 to 120
        :return: the stat, float number
        """
        statID -= 1
        if level < 1 or level > 120:
            raise ValueError("Level out of bound")
        else:
            if level <= 100:
                return self.attrs[statID] + (level - 1) * self.attrsGrowth[statID] / 1000
            else:
                return self.attrs[statID] + (level - 1) * self.attrsGrowth[statID] / 1000 + \
                       (level - 100) * self.attrsGrowthExtra[statID] / 1000

    def getStar(self) -> int:
        """
        get the star of this ship

        :return: star, integer
        """
        return self.star

    def getRarity(self) -> int:
        """
        get the rarity of this ship

        :return: rarity, integer, common: 1, rare: 2, elite: 3, super rare: 4, PR: 5, DR: 6
        """
        return self.rarity

    def getName(self) -> str:
        """
        get the name of this ship

        :return: name, string
        """
        return self.name

    def getEnglishName(self) -> str:
        """
        get the English name of this ship

        :return: name with prefix, string
        """
        return self.englishName

    def getHullType(self) -> int:
        """
        get the hull type number of this ship

        :return: hull type number, integer, range from 1 to 18
        """
        return self.hullType

    def getID(self) -> int:
        """
        get the id of this ship

        :return: id, integer
        """
        return self.id

    def getEquipmentProficiency(self, equipSlot: int) -> float:
        """
        get the equipment proficiency of a certain slot (including the fixed weapon for torpedo ships)

        :param equipSlot: the specific slot, integer, range from 1 - 4, 1 is the first weapon, 4 is the fixed weapon
                          on all torpedo ships
        :return: the proficiency, float number
        """
        return self.proficiency[equipSlot - 1]

    def getEquipBase(self, equipSlot: int) -> int:
        """
        get the equipment base count of a certain slot

        :param equipSlot: the specific slot, integer, range from 1 - 3, 1 is the first weapon
        :return: the base count, integer
        """
        return self.equipBaseList[equipSlot - 1]

    def getSkillList(self) -> List[int]:
        """
        get the skill list of this ship

        :return: skill list, list of integer
        """
        return self.skillList

    def getEquipmentType(self, equipSlot: int) -> List[int]:
        """
        get the equipment type of a specific slot

        :param equipSlot: the specific slot, integer, range from 0 to 4
        :return: equipment type, integer
        """
        if equipSlot in [1, 2, 3, 4, 5]:
            return self.equipTypeList[equipSlot - 1]
        else:
            raise ValueError("equipSlot ({}) should be 1 - 5".format(equipSlot))

    def toString(self) -> str:
        string = "Name: {name}{kagaBB} ({nameWithPrefix})\n".format(name=self.name,
                                                                    kagaBB=" BB" if isKagaBB(self.id) else "",
                                                                    nameWithPrefix=self.englishName) + \
                 "ID: {id}\n".format(id=self.id) + \
                 "HullType: {hullType}\n".format(hullType=self.hullType) + \
                 "Rarity: {rarity}\n".format(rarity=self.rarity) + \
                 "Stars: {stars}\n".format(stars=self.star) + \
                 "Skills: {skill}\n".format(skill=self.skillList) + \
                 "EquipType: {equips}\n".format(equips=self.equipTypeList) + \
                 "EquipBase: {equipBase}\n".format(equipBase=self.equipBaseList)
        return string


class SurfaceShip(Ship):
    def __init__(self, statDict: dict, dataDict: dict):
        super(SurfaceShip, self).__init__(statDict, dataDict)
        self.isSubmarine = False
        self.isSurfaceShip = True


class Submarine(Ship):
    def __init__(self, statDict: dict, dataDict: dict):
        super(Submarine, self).__init__(statDict, dataDict)
        self.isSubmarine = True
        self.isSurfaceShip = False
        self.oxygen = statDict["oxy_max"]
        self.oxyCost = statDict["oxy_cost"]
        self.oxyRecovery = statDict["oxy_recovery"]
        self.ammo = statDict["ammo"]
        self.surfaceDuration = statDict["attack_duration"]
        self.huntingRangeLevel = statDict["huntingrange_level"]
        self.huntingRange = statDict["hunting_range"]

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
