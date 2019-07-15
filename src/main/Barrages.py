from typing import Dict


class Barrage:
    """
    Barrage class describes in what pattern are the projectiles (bullets) created
    """

    def __init__(self, barrageData: Dict):
        self.id = barrageData["id"]
        self.offsetZ = barrageData["offset_z"]
        self.deltaOffsetZ = barrageData["delta_offset_z"]
        self.offsetX = barrageData["offset_x"]
        self.deltaOffsetX = barrageData["delta_offset_x"]
        self.angle = barrageData["angle"]
        self.deltaAngle = barrageData["delta_angle"]
        self.delayCast = barrageData["first_delay"]
        self.primalDelay = barrageData["delay"]
        self.deltaPrimalDelay = barrageData["delta_delay"]
        self.primalRepeat = barrageData["primal_repeat"]
        self.seniorDelay = barrageData["senior_delay"]
        self.seniorRepeat = barrageData["senior_repeat"]
        self.randomAngle = barrageData["random_angle"]
        self.offsetPrioritise = barrageData["offset_prioritise"]

    def getProjectileCount(self) -> int:
        """
        Calculates the total projectiles created

        :return: integer, the projectiles count
        """
        return (self.seniorRepeat + 1) * (self.primalRepeat + 1)

    def getAnimationTime(self) -> float:
        """
        Calculates the firing animation time (from barrage start to the last wave being fired)

        :return: float, the total animation time
        """
        return self.delayCast + (self.primalDelay * self.primalRepeat + max(0, 1 / 2 * (self.primalRepeat - 1) * (
                self.primalRepeat - 2) * self.deltaPrimalDelay)) * (
                       self.seniorRepeat + 1) + self.seniorDelay * self.seniorRepeat
