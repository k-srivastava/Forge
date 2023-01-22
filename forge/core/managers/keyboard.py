"""
Keyboard management in Forge.
"""
import enum
import typing

import pygame

import forge.core.engine.game

DISABLED = False


class Key(enum.IntEnum):
    """
    Keys with direct-wrapping to Pygame's key-codes; which themselves are wrapped for SDL key codes.
    """
    # Alphabets.
    A = 97
    B = 98
    C = 99
    D = 100
    E = 101
    F = 102
    G = 103
    H = 104
    I = 105
    J = 106
    K = 107
    L = 108
    M = 109
    N = 110
    O = 111
    P = 112
    Q = 113
    R = 114
    S = 115
    T = 116
    U = 117
    V = 118
    W = 119
    X = 120
    Y = 121
    Z = 122

    # Numbers on the top-row.
    NUM_0 = 48
    NUM_1 = 49
    NUM_2 = 50
    NUM_3 = 51
    NUM_4 = 52
    NUM_5 = 53
    NUM_6 = 54
    NUM_7 = 55
    NUM_8 = 56
    NUM_9 = 57

    # Numbers on the number-pad.
    KEYPAD_NUM_0 = 1073741922
    KEYPAD_NUM_1 = 1073741913
    KEYPAD_NUM_2 = 1073741914
    KEYPAD_NUM_3 = 1073741915
    KEYPAD_NUM_4 = 1073741916
    KEYPAD_NUM_5 = 1073741917
    KEYPAD_NUM_6 = 1073741918
    KEYPAD_NUM_7 = 1073741919
    KEYPAD_NUM_8 = 1073741920
    KEYPAD_NUM_9 = 1073741921

    # Mathematical operators on the number-pad.
    KEYPAD_DIVIDE = 1073741908
    KEYPAD_ENTER = 1073741912
    KEYPAD_EQUALS = 1073741927
    KEYPAD_MINUS = 1073741910
    KEYPAD_MULTIPLY = 1073741909
    KEYPAD_PERIOD = 1073741923
    KEYPAD_PLUS = 1073741911

    # Arrow keys.
    UP = 1073741906
    DOWN = 1073741905
    LEFT = 1073741904
    RIGHT = 1073741903

    # Function keys.
    F1 = 1073741882
    F2 = 1073741883
    F3 = 1073741884
    F4 = 1073741885
    F5 = 1073741886
    F6 = 1073741887
    F7 = 1073741888
    F8 = 1073741889
    F9 = 1073741890
    F10 = 1073741891
    F11 = 1073741892
    F12 = 1073741893
    F13 = 1073741928
    F14 = 1073741929
    F15 = 1073741930

    # Left-hand side modifier keys.
    LEFT_ALT = 1073742050
    LEFT_CTRL = 1073742048
    LEFT_BRACKET = 91
    LEFT_PAREN = 40
    LEFT_SHIFT = 1073742049

    # Right-hand side modifier keys.
    RIGHT_ALT = 1073742054
    RIGHT_CTRL = 1073742052
    RIGHT_BRACKET = 93
    RIGHT_PAREN = 41
    RIGHT_SHIFT = 1073742053

    # Remaining keys.
    AMPERSAND = 38
    ASTERISK = 42
    AT = 64
    BACK_QUOTE = 96
    BACKSLASH = 92
    BACKSPACE = 8
    BREAK = 1073741896
    CAPS_LOCK = 1073741881
    CARET = 94
    CLEAR = 1073741980
    COLON = 58
    COMMA = 44
    CURRENCY_SUBUNIT = 1073742005
    CURRENCY_UNIT = 1073742004
    DELETE = 127
    DOLLAR = 36
    END = 1073741901
    EQUALS = 61
    ESCAPE = 27
    EURO = 1073742004
    EXCLAMATION_MARK = 33
    GREATER = 62
    HASH = 35
    HELP = 1073741941
    HOME = 1073741898
    INSERT = 1073741897
    LESS = 60
    MENU = 1073741942
    MINUS = 45
    MODE = 1073742081
    NUM_LOCK = 1073741907
    PAGE_DOWN = 1073741902
    PAGE_UP = 1073741899
    PAUSE = 1073741896
    PERCENT = 37
    PERIOD = 46
    PLUS = 43
    POWER = 1073741926
    PRINT = 1073741894
    PRINT_SCREEN = 1073741894
    QUESTION_MARK = 63
    QUOTE = 39
    RETURN = 13
    SCROLL_LOCK = 1073741895
    SEMICOLON = 59
    SLASH = 47
    SPACE = 32
    TAB = 9
    UNDERSCORE = 95

    UNKNOWN = 0


def is_clicked(key: Key) -> bool:
    """
    Check if a certain keyboard key is pressed once.

    :param key: Enum value of the key to check.
    :type key: Key

    :return: True if the keyboard key is pressed once; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    game = forge.core.engine.game.get_game()

    if game is not None:
        for event in game.event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == key.value:
                    return True

    return False


# noinspection DuplicatedCode
def is_any_clicked() -> bool:
    """
    Check if any keyboard key is pressed once.

    :return: True if any keyboard key is pressed once; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    game = forge.core.engine.game.get_game()

    if game is not None:
        for event in game.event_list:
            if event.type == pygame.KEYDOWN:
                return True

    return False


def is_pressed(key: Key) -> bool:
    """
    Check if a certain key is pressed continuously.

    :param key: Enum value of the key to check.
    :type key: Key

    :return: True if the keyboard key is pressed continuously; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    return pygame.key.get_pressed()[key.value]


def is_any_pressed() -> bool:
    """
    Check if any keyboard key is pressed continuously.

    :return: True if any keyboard key is pressed continuously; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    return any(pygame.key.get_pressed())


def is_none_pressed() -> bool:
    """
    Check if no keyboard key is pressed continuously.

    :return: True if no keyboard key is pressed continuously; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    keys = pygame.key.get_pressed()

    for key in keys:
        if key:
            return False

    return True


def get_all_pressed() -> typing.Sequence[bool]:
    """
    Get all the keys of the keyboard.

    :return: All the keys that are pressed.
    :rtype: typing.Sequence[bool]
    """
    if DISABLED:
        return pygame.key.ScancodeWrapper()

    return pygame.key.get_pressed()
