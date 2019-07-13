from typing import Dict


class ResearchStrengthenNode:
    def __init__(self, effectData: dict, reversedAttrDict: Dict[str, int]):
        self.id = effectData["id"]
        self.devLevel = effectData["lv"]
        self.requiredLevel = effectData["need_lv"]
        self.description = effectData["effect_desc"]
        self.dialogUnlocked = effectData["effect_dialog"]
        self.expNeeded = effectData["need_exp"]
        self.preloadList = effectData["effect_preload"]
        self.proficiencyBonus = effectData["effect_equipment_proficiency"]

        attrList = effectData["effect_attr"]
        self.statBonus = {reversedAttrDict[attrBonus[0]]: attrBonus[1] for attrBonus in attrList}

    def getStatBonus(self, statId: int) -> int:
        """
        Gets the stat bonus of a certain stat

        :param statId: integer, range from 1 to 12, the stat id
        :return: integer, the bonus value
        """
        return self.statBonus.get(statId, 0)

    def getEquipProficiencyBonus(self, slotId: int) -> float:
        if len(self.proficiencyBonus) == 0:
            return 0
        else:
            return self.proficiencyBonus[1] if self.proficiencyBonus[0] == slotId else 0
