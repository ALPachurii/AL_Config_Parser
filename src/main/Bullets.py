from typing import *


class Bullet:
    """
    Bullet class describes the behavior and attribute of one single projectile
    """

    def __init__(self, bulletData: Dict):
        self.id = bulletData["id"]
        self.type = bulletData["type"]  # 1: Normal Projectiles, 2: Projectiles that travel in a parabola, 3: Torpedoes
        self.velocity = bulletData["velocity"]
        self.ammoType = bulletData["ammo_type"]  # 1: Normal, 2: 2: AP, 3: HE, 4: Torpedo
        self.armorModifier = bulletData["damage_type"]
        self.range = bulletData["range"]
        self.rangeOffset = bulletData["rangeOffset"]
        self.pierceCount = bulletData["pierce_count"]
        self.canPierce = self.pierceCount != 0
        self.extraParam = bulletData["extra_param"]

    def getType(self) -> int:
        """
        Gets the bullet traveling/rendering type

        :return: integer, 1 means normal projectiles (not affected by gravity), 2 means projectiles traveling in a
                 parabola, 3 means torpedoes
        """
        return self.type

    def getAmmoType(self) -> int:
        """
        Gets the bullet ammo type

        :return: integer, 1 means normal, 2 means AP, 3 means HE, 4 means torpedo
        """
        return self.ammoType

    def getVelocity(self) -> int:
        """
        Gets the projectile velocity

        :return: integer, the velocity
        """
        return self.velocity

    def getArmorModifier(self, armorType: int) -> float:
        """
        Gets the armor modifier of a certain armor type

        :param armorType: integer, range from 0 - 2, 0 means light, 2 means medium, 3 means heavy
        :return: float number, the armor modifier
        """
        return self.armorModifier[armorType]

    def getPierceCount(self) -> int:
        """
        Gets the number of enemies this bullet can pierce through

        :return: integer, pierce limit, always larger or equal than 0
        """
        return self.pierceCount
