from typing import *
from functools import reduce
from re import sub
from .ConfigParser import ConfigParser
from .Weapons import Weapon


class Triggerable:
    """
    Triggerable objects represents the triggerable skills and buffs in game. They have attribute effectList that
    describes the effect when being triggered and the trigger condition though this class has ignored all trigger
    condition and all effect except creating a barrage. They are ordered in a tree like structure.
    """

    def __init__(self, data: Dict, level: int, parser: ConfigParser):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["desc"]
        self.level = level
        if str(level) in data and "effect_list" in data[str(level)]:
            self.effectList = data[str(level)]["effect_list"]
        else:
            self.effectList = data["effect_list"]

        self.childBuffs = []
        self.childSkills = []
        self.dotEffects = []
        self.weapons = []

        self.containsWeapons = False

    def getId(self) -> int:
        """
        Gets the id of this triggerable object
        :return:
        """

        return self.id

    def getName(self) -> str:
        """
        Gets the name of this triggerable object

        :return:
        """

        return self.name

    def getDescription(self) -> str:
        """
        Gets the description of this triggerable object

        :return:
        """
        return self.description

    def getLevel(self) -> int:
        """
        Gets the level of this triggerable object

        :return:
        """
        return self.level

    def getWeaponList(self) -> List[Weapon]:
        """
        Gets the list of weapons that this triggerable object might trigger

        :return: list of weapons. each weapon is a barrage generator
        """
        return self.weapons


class Skill(Triggerable):
    """
    Skills are basically a collection of skill effects
    """

    def __init__(self, skillData: Dict, skillLevel: int, parser: ConfigParser):
        super(Skill, self).__init__(skillData, skillLevel, parser)
        for effect in self.effectList:
            effectType = effect["type"]
            argList = effect["arg_list"]
            if effectType == "BattleSkillAddBuff":
                self.childBuffs.append(parser.getBuff(argList["buff_id"], skillLevel))
            elif effectType == "BattleSkillFire":
                weaponId = argList["weapon_id"]
                self.weapons.append(parser.getWeapon(weaponId))
                self.containsWeapons = True

        self.containsWeapons = self.containsWeapons or any(map(lambda x: x.containsWeapons, self.childBuffs))
        self.weapons += reduce(lambda x, y: x + y, map(lambda x: x.weapons, self.childBuffs), [])
        self.dotEffects += reduce(lambda x, y: x + y, [buff.dotEffects for buff in self.childBuffs], []) + \
            reduce(lambda x, y: x + y, [skill.dotEffects for skill in self.childSkills], [])
        self.isLeaf = len(self.childBuffs) == 0


class Buff(Triggerable):
    """
    Buffs are generally the control layer of skill tree that control the triggering of skill effects
    """

    def __init__(self, buffData: Dict, buffLevel: int, parser: ConfigParser):
        self.icon = buffData["icon"]
        super(Buff, self).__init__(buffData, buffLevel, parser)
        for effect in self.effectList:
            effectType = effect["type"]
            argList = effect["arg_list"]
            if effectType == "BattleBuffAddBuff":
                self.childBuffs.append(parser.getBuff(argList["buff_id"], self.level))
            elif effectType == "BattleBuffCastSkill":
                self.childSkills.append(parser.getSkill(argList["skill_id"], self.level))
            elif effectType == "BattleBuffCastSkillRandom":
                self.childSkills += [parser.getSkill(skillId, self.level) for skillId in argList["skill_id_list"]]
            elif effectType == "BattleBuffDOT":
                self.dotEffects += argList

        self.dotEffects += reduce(lambda x, y: x + y, [buff.dotEffects for buff in self.childBuffs], []) + \
            reduce(lambda x, y: x + y, [skill.dotEffects for skill in self.childSkills], [])

        self.containsWeapons = any(map(lambda x: x.containsWeapons, self.childBuffs)) or any(
            map(lambda x: x.containsWeapons, self.childSkills))
        self.weapons = reduce(lambda x, y: x + y, map(lambda x: x.weapons, self.childBuffs), []) + reduce(
            lambda x, y: x + y, map(lambda x: x.weapons, self.childSkills), [])
        self.isLeaf = len(self.childBuffs) == 0 and len(self.childSkills) == 0

    def getIcon(self) -> int:
        """
        Gets the buff icon id

        :return: integer, the icon id
        """
        return self.icon


class RootBuff(Buff):
    """
    RootBuffs are the root nodes of skill trees. They represents the visible skills in-game.
    """

    def __init__(self, buffData: Dict, skillData: Dict, parser: ConfigParser):
        self.maxLevel = skillData["max_level"]
        super(RootBuff, self).__init__(buffData, self.maxLevel, parser)
        desc = skillData["desc"]
        self.descriptionUponUnlocking = skillData["desc_get"]
        descAdd = skillData["desc_add"]
        withIndex = zip(descAdd, range(1, 10))
        for paramList, index in withIndex:
            desc = sub(r"\${}".format(index), "{} ({})".format(paramList[0][0], paramList[self.maxLevel - 1][0]), desc)
        self.name = skillData["name"]
        self.id = skillData["id"]
        self.type = skillData["type"]
        self.description = desc

    def getType(self) -> int:
        """
        Gets the skill type of this buff

        :return: integer, range from 1-3, the skill type, 1 for offensive, 2 for defensive and 3 for support
        """
        return self.type
