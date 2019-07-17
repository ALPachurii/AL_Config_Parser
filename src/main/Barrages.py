from typing import Dict


class Barrage:
    """
    Barrage class describes in what pattern are the projectiles (bullets) created
    """

    def __init__(self, barrageData: Dict):
        self.id = barrageData["id"]
        self.offsetZ = barrageData.get("offset_z")
        self.deltaOffsetZ = barrageData.get("delta_offset_z")
        self.offsetX = barrageData.get("offset_x")
        self.deltaOffsetX = barrageData.get("delta_offset_x")
        self.angle = barrageData.get("angle")
        self.deltaAngle = barrageData.get("delta_angle")
        self.delayCast = barrageData.get("first_delay")
        self.primalDelay = barrageData.get("delay")
        self.deltaPrimalDelay = barrageData.get("delta_delay")
        self.primalRepeat = barrageData.get("primal_repeat")
        self.seniorDelay = barrageData.get("senior_delay")
        self.seniorRepeat = barrageData.get("senior_repeat")
        self.randomAngle = barrageData.get("random_angle")
        self.offsetPrioritise = barrageData.get("offset_prioritise")

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
