
def in_enum(item, enumeration) -> bool:
    """
    :param enumeration: The enumeration class
    :param item: item to compare against Enum
    :return:
    """
    try:
        return item in enumeration
    except (KeyError, TypeError) as _:
        if isinstance(item, str):
            return (item in [i.value for i in enumeration]) or (item in [i.name for i in enumeration])
    return False