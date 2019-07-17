from math import sqrt
from typing import *
from .ConfigParser import ConfigParser


class Weapon:
    """
    Weapon class describes the attributes of in-game weapon and has methods to calculate damage etc.
    """

    def __init__(self, weaponData: Dict, parser: ConfigParser):
        self.id = weaponData["id"]
        if "base" in weaponData:
            self.base = parser.getWeapon(weaponData["base"])
        else:
            self.base = None
        self.name = weaponData.get("name") or self.base.name

        self.spawnType = weaponData.get("spawn_bound") or self.base.spawnType

        self.barrages = [parser.getBarrage(barrageId) for barrageId in
                         weaponData.get("barrage_ID", [])] or self.base.barrages
        self.barrageIdList = weaponData.get("barrage_ID") or self.base.barrageIdList

        if self.spawnType in ["cannon", "antiaircraft", "torpedo"]:
            self.bullets = [parser.getBullet(bulletId) for bulletId in
                            weaponData.get("bullet_ID", [])] or self.base.bullets
        elif self.spawnType == "plane":
            try:
                self.bullets = [parser.getAircraft(bulletId) for bulletId in
                                weaponData.get("bullet_ID", [])]
            except KeyError:
                try:
                    self.bullets = [parser.getAircraft(self.id)]
                except KeyError:
                    self.bullets = self.base.bullets
        else:
            raise ValueError("unknown spawnType ({})".format(self.spawnType))

        self.bulletIdList = weaponData.get("bullet_ID") or self.base.bulletIdList

        self.sameBullet = all([self.bulletIdList[0] == bulletId for bulletId in self.bulletIdList])
        self.barragesWithBullets = zip(self.barrages, self.bullets)

        self.type = weaponData.get("type") or self.base.type
        self.damage = weaponData.get("damage") or self.base.damage
        if "attack_attribute" in weaponData:
            self.modifierStat = weaponData["attack_attribute"]
        else:
            self.modifierStat = self.base.modifierStat
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
        if self.spawnType == "cannon" or self.spawnType == "torpedo":
            return sum([barrage.getProjectileCount() * self.damage for barrage in self.barrages])
        elif self.spawnType == "plane":
            return sum(
                [barrage.getProjectileCount() * sum([weapon.getRawDamageSum() for weapon in bullet.getWeapons()]) for
                 barrage, bullet in self.barragesWithBullets])
        else:
            return 0

    def getDamageSumByArmorType(self, armorType: int) -> float:
        """
        Calculates the sum of damage dealt to a certain armor type, considering both armor modifier and weapon
        coefficient but not the modifier stat

        :param armorType: integer, range from 1-3, the armor type. 1 for light, 2 for medium and 3 for heavy
        :return: float, the total damage
        """
        if self.spawnType == "cannon" or self.spawnType == "torpedo":
            return sum([
                barrage.getProjectileCount() * bullet.getArmorModifier(armorType) * self.damage for barrage, bullet in
                self.barragesWithBullets]) * self.coefficient
        elif self.spawnType == "plane":
            return sum([
                barrage.getProjectileCount() * sum([
                    weapon.getDamageSumByArmorType() for weapon in bullet.getWeapons()]) for
                barrage, bullet in self.barragesWithBullets
            ]) * self.coefficient
        else:
            return 0

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
            if self.spawnType in ["cannon", "torpedo"]:
                return self.bullets[0].getAmmoType()
            elif self.spawnType == "plane":
                weapons = self.bullets[0].getWeapons()
                ammoType = weapons[0].getAmmoType()
                sameAmmoType = True
                for weapon in weapons:
                    if weapon.getAmmoType() is not None and weapon.getAmmoType() != ammoType:
                        sameAmmoType = False
                if sameAmmoType:
                    return ammoType

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
