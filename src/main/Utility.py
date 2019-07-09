def isFiltered(ID: int) -> bool:
    """
    check whether a shipID should be filtered
    :param ID: shipID
    :return: bool
    """
    return 900000 <= ID <= 901000


def isKagaBB(ID: int) -> bool:
    """
    check if this ship is Kaga BB
    :param ID:
    :return:
    """
    return str(ID)[slice(0, 5)] == "30507"


def getMetaID(ID: int) -> int:
    """
    get the id of the meta ship of this ship
    :param ID:
    :return:
    """
    return int(str(ID)[slice(0, -1)])
