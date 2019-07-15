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
        self.primalRepeat = barrageData["primal_repeat"]
        self.seniorDelay = barrageData["senior_delay"]
        self.seniorRepeat = barrageData["senior_repeat"]
        self.randomAngle = barrageData["random_angle"]
        self.offsetPrioritise = barrageData["offset_prioritise"]

    def getProjectileCount(self) -> int:
        """
        Calculates the total projectiles created

        :return: integer the projectiles count
        """
        return (self.seniorRepeat + 1) * (self.primalRepeat + 1)
