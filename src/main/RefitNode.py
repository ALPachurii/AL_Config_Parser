from typing import Dict, Any, List


class RefitNode:
    def __init__(self, nodeDict: Dict[str, Any], reversedAttrDict: Dict[str, int]):
        self.id: int = nodeDict["id"]
        self.goldNeeded: int = nodeDict["use_gold"]
        self.levelLimit: int = nodeDict["level_limit"]
        self.starLimit: int = nodeDict["star_limit"]
        self.maxLevel: int = nodeDict["max_level"]
        self.useShip: bool = nodeDict["use_ship"] == 1
        self.icon: str = nodeDict["icon"]
        self.name: str = nodeDict["name"]
        self.bonus: List[Dict[int, int]] = [{reversedAttrDict[attrName]: value for attrName, value in attrDict.items()}
                                            for attrDict in nodeDict["effect"]]
        self.itemConsumption: List[List[List[int]]] = nodeDict["use_item"]
        self.ratingBonus: List[int] = nodeDict["gear_score"]
        self.parents: List[int] = nodeDict["condition_id"]

    def getId(self) -> int:
        return self.id

    def getParents(self) -> List[int]:
        return self.parents

    def getName(self) -> str:
        return self.name

    def getIconName(self) -> str:
        return self.icon

    def getMaxLevel(self) -> int:
        return self.maxLevel

    def getItemConsumption(self, stage: int) -> List[List[int]]:
        """
        Gets the item consumption of a certain stage of this node

        :param stage: integer, range from 1 to maxLevel, the stage of this node
        :return: List of List of integer, structure: [[item1Id, number of items], [item2Id, number of items], ...]
        """
        return self.itemConsumption[stage - 1]

    def getItemConsumptionList(self) -> List[List[List[int]]]:
        """
        Gets the raw item consumption list of this node

        :return: List of List of List of integer, structure: [[[item1Id, number of items], ...], ...]
        """

    def getStarLimit(self) -> int:
        return self.starLimit

    def getGoldNeeded(self) -> int:
        return self.goldNeeded

    def getLevelLimit(self) -> int:
        return self.levelLimit

    def getStatBonus(self, stage: int, statId: int) -> int:
        """
        Gets the bonus of a certain stat from a certain stage of refit

        :param stage: integer, range from 1 to malLevel, the stage of this node
        :param statId: integer, range from 1 to 12, the id of that stat
        :return: integer, the bonus, 0 means no bonus
        """
        return self.bonus[stage - 1].get(statId, 0)

    def getStatBonusSum(self, statId: int) -> int:
        """
        Calculates the sum of bonuses to a certain stat from all stages of this refit node

        :param statId: integer, range from 1 to 12, the id of that stat
        :return: integer, the bonus, 0 means no bonus
        """
        return sum([self.bonus[level].get(statId, 0) for level in range(0, self.maxLevel)])

    def getStatBonusList(self) -> List[Dict[int, int]]:
        """
        Gets the raw stat bonus list

        :return: List of Map from integer to integer, structure [{statId1: value1, statId2: value2, ..}, ..]
        """
        return self.bonus

        pass
