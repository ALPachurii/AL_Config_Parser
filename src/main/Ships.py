import math
from typing import List, Dict, Generic, TypeVar, Tuple


class Ship:
    def __init__(self, statDict: dict, dataDict: dict, fleetTechStat: dict):
        self.nationality = statDict["nationality"]
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

        self.fleetTechPoint = [fleetTechStat["pt_get"], fleetTechStat["pt_upgrage"], fleetTechStat["pt_level"]]
        self.fleetStatBonus = [{"attr": fleetTechStat["add_get_attr"], "value": fleetTechStat["add_get_value"]},
                               {"attr": fleetTechStat["add_level_attr"], "value": fleetTechStat["add_level_value"]}]

        self.equipTypeList = [dataDict["equip_1"], dataDict["equip_2"], dataDict["equip_3"], dataDict["equip_4"],
                              dataDict["equip_5"]]
        self.skillList = dataDict["buff_list_display"]

    def getStat(self, statID: int, level: int, affBonus: int) -> float:
        if level < 1 or level > 120:
            raise ValueError("Level out of bound")
        elif affBonus < 0 or affBonus > 12:
            raise ValueError("affBonus out of bound")
        else:
            if level <= 100:
                return self.attrs[statID] + (level - 1) * self.attrsGrowth[statID] / 1000
            else:
                return self.attrs[statID] + (level - 1) * self.attrsGrowth / 1000 + \
                       (level - 100) * self.attrsGrowthExtra / 1000

    def getFlooredStat(self, statID: int, level: int, affBonus: int) -> int:
        return math.floor(self.getStat(statID, level, affBonus))

    def getStar(self) -> int:
        return self.star

    def getRarity(self) -> int:
        return self.rarity

    def getName(self) -> str:
        return self.name

    def getEnglishName(self) -> str:
        return self.englishName

    def getHullType(self) -> int:
        return self.hullType

    def getID(self) -> int:
        return self.id

    def getEquipmentProficiency(self, equipSlot: int) -> float:
        return self.proficiency[equipSlot]

    def getBaseEquip(self) -> list:
        return self.equipBaseList

    def getFleetTechPoint(self, stage: int) -> int:
        if stage == 0 or stage == 1 or stage == 2:
            return self.fleetTechPoint[stage]
        else:
            raise ValueError("stage should be 0 - 2")

    def getFleetStatBonus(self, stage: int) -> Tuple[int, int]:
        if stage == 0 or stage == 1:
            return self.fleetStatBonus[stage]["attr"], self.fleetStatBonus[stage]["value"]
        else:
            raise ValueError("stage should be 0 or 1")

    def getSkillList(self) -> List[int]:
        return self.skillList

    def getEquipmentType(self, equipSlot: int) -> int:
        if equipSlot in [0, 1, 2, 3, 4]:
            return self.equipTypeList[equipSlot]
        else:
            raise ValueError("equipSlot should be 0-4")

    def toString(self):
        pass


class SurfaceShip(Ship):
    def __init__(self, statDict: dict, dataDict: dict, fleetTechStat: dict):
        super(SurfaceShip, self).__init__(statDict, dataDict, fleetTechStat)
        self.isSubmarine = False
        self.isSurfaceShip = True

    def isSubmarine(self) -> bool:
        return self.isSubmarine

    def isSurfaceShip(self) -> bool:
        return self.isSurfaceShip


class Submarine(Ship):
    def __init__(self, statDict: dict, dataDict: dict, fleetTechStat: dict):
        super(Submarine, self).__init__(statDict, dataDict, fleetTechStat)
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
        return self.isSubmarine

    def isSurfaceShip(self) -> bool:
        return self.isSurfaceShip

    def getOxygen(self) -> int:
        return self.oxygen

    def getOxyCost(self) -> int:
        return self.oxyCost

    def getAmmo(self) -> int:
        return self.ammo

    def getHuntingRange(self) -> List[List[List[int]]]:
        return self.huntingRange

    def getHuntingRangeLevel(self) -> int:
        return self.huntingRangeLevel

    pass
