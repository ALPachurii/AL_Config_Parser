from math import sqrt
from typing import *
from .ConfigParser import ConfigParser


class Weapon:
    """
    Weapon class describes the attributes of in-game weapon and has methods to calculate damage etc.
    """
    def __init__(self, weaponData: Dict, parser: ConfigParser):
        self.id = weaponData["id"]
        self.name = weaponData["name"]
        if "base" in weaponData:
            self.base = parser.getWeapon(weaponData["base"])
        else:
            self.base = None

        self.barrages = [parser.getBarrage(barrageId) for barrageId in
                         weaponData.get("barrage_ID", [])] or self.base.barrages
        self.barrageIdList = weaponData.get("barrage_ID") or self.base.barrageIdList

        self.bullets = [parser.getBullet(bulletId) for bulletId in
                        weaponData.get("bullet_ID", [])] or self.base.bullets
        self.bulletIdList = weaponData.get("bullet_ID") or self.base.bulletIdList

        self.sameBullet = all([self.bulletIdList[0] == bulletId for bulletId in self.bulletIdList])
        self.barragesWithBullets = zip(self.barrages, self.bullets)

        self.type = weaponData.get("type") or self.base.type
        self.damage = weaponData.get("damage") or self.base.damage
        self.modifierStat = (weaponData.get("attack_attribute") or self.base.modifierStat - 1) + 1
        self.modifierStatRatio = (weaponData.get("attack_attribute_ratio") or self.base.modifierStatRatio * 100) / 100
        self.reload = self.base.reload if self.base else weaponData["reload_max"] / (12 * sqrt(157))
        self.range = weaponData.get("range") or self.base.range
        self.angle = weaponData.get("angle") or self.base.angle
        self.coefficient = weaponData.get("corrected") or self.base.coefficient

    def getWeaponModifier(self) -> float:
        """
        Gets the modifier/coefficient of this weapon

        :return: float, the coefficient
        """
        return self.coefficient

    def getDamage(self) -> int:
        """
        Gets the raw damage of a single projectile

        :return: integer, the damage
        """
        return self.damage

    def getModifierStat(self) -> int:
        """
        Gets the id of the stat that modifies the damage

        :return: integer, the statId of that stat
        """
        return self.modifierStat

    def getModifierStatRatio(self) -> float:
        """
        Gets the ratio of the modifier stat that is counted

        :return: float number, the ratio
        """
        return self.modifierStatRatio

    def getRawDamageSum(self) -> int:
        """
        Calculates the sum of the raw damage of all projectiles

        :return: integer, the sum
        """
        return sum([barrage.getProjectileCount() * self.damage for barrage in self.barrages])

    def getDamageSumByArmorType(self, armorType: int) -> float:
        """
        Calculates the sum of damage dealt to a certain armor type, considering both armor modifier and weapon
        coefficient but not the modifier stat

        :param armorType: integer, range from 1-3, the armor type. 1 for light, 2 for medium and 3 for heavy
        :return: float, the total damage
        """
        return sum([
            barrage.getProjectileCount() * bullet.getArmorModifier(armorType) * self.damage for barrage, bullet in
            self.barragesWithBullets]) * self.coefficient

    def getProjectilesByAmmoType(self, ammoType: int) -> int:
        """
        Gets the projectile count of a certain ammo type

        :param ammoType: the ammo type, see Bullets class for more info
        :return: integer, the total projectiles
        """
        return sum([
            barrage.getProjectileCount() if bullet.getAmmoType() == ammoType else 0 for barrage, bullet in
            self.barragesWithBullets])

    def getType(self) -> Optional[int]:
        """
        Gets the bullet traveling/rendering type if all bullets are the same, else returns None

        :return: integer represents the projectile type and None means different bullets
        """
        if self.sameBullet:
            return self.bullets[0].getType()

    def getAmmoType(self) -> Optional[int]:
        """
        Gets the ammo type if all bullets are the same, else returns None

        :return: integer or None, integer represents the ammo type and None means different bullets
        """
        if self.sameBullet:
            return self.bullets[0].getAmmoType()

    def getArmorModifier(self, armorType: int) -> Optional[float]:
        """
        Gets the armor modifier against a certain armor type if all bullets are the same, else returns None

        :param armorType: integer, range from 1-3, the armor type, see Bullets class for more info
        :return: float or None, float represents the armor modifier and None means different bullets
        """
        if self.sameBullet:
            return self.bullets[0].getArmorModifier(armorType)


class Aircraft:
    """
    Aircraft are somewhat like bullets in the sense of it can also be generated by weapon. But it can also carry
    weapons, namely aircraft based torpedoes, bombs and AA guns.
    """
    def __init__(self, weaponData: Dict, parser: ConfigParser):
        self.id = weaponData["id"]
        self.name = weaponData["name"]
        if "base" in weaponData:
            self.base = parser.getAircraft(weaponData["base"])
        else:
            self.base = None

        self.type = weaponData.get("type") or self.base.type
        self.maxHp = weaponData.get("max_hp") or self.base.maxHp
        self.hpGrowth = weaponData.get("hp_growth") or self.base.hpGrowth  # hp = maxHp + (level - 1) * hpGrowth / 1000
        self.crashDamage = weaponData.get("crash_DMG") or self.base.crashDamage
        self.evaRate = weaponData.get("dodge") or self.base.evaRate
        self.speed = weaponData.get("speed") or self.base.speed
        self.weapons = [parser.getWeapon(weaponId) for weaponId in weaponData.get("weapon_ID")] or self.base.weapons

    def getWeapons(self) -> List[Weapon]:
        """
        Gets a list of weapons this aircraft is carrying

        :return: list of Weapon
        """
        return self.weapons
