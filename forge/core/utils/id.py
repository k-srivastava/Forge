"""
Forge's ID system. The uniqueness of each ID is maintained on a global, project-wide level.
"""
import random
import string

import forge.core.utils.exceptions

_IDS: set[int] = set()


def generate_random_id(length: int = 8) -> int:
    """
    Generate a new unique random ID of a given length.

    :param length: Length of the ID to be generated.
    :type length: int

    :return: New random and unique ID.
    :rtype: int
    """
    while True:
        id_ = int(''.join(random.choices(string.digits, k=length)))

        if id_ not in _IDS:
            break

    _IDS.add(id_)
    return id_


def delete_id(id_: int) -> None:
    """
    Delete an ID making it free to be randomly generated again. Often used when an object associated with the given ID
    is also deleted.

    :param id_: ID to be deleted.
    :type id_: int

    :raises forge.core.utils.exceptions.IDNotFoundError: An ID must be registered if it is to be deleted.
    """
    if id_ not in _IDS:
        raise forge.core.utils.exceptions.IDNotFoundError(id_)

    _IDS.remove(id_)
