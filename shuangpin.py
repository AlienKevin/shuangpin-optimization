import json
from enum import Enum, IntEnum

# first: 0 = left hand, 1 = right hand
# second: 1 = index finger, 2 = index finger, 3 = middle finger, 4 = ring finger, 5 = little finger
# third: 0 = upper row, 1 = home row, 2 = bottom row
Location = tuple[int, int, int]

Key = str

# Fixed keyboard layout inherited from QWERTY

qwerty_layout: dict[Key, Location] = {
    # 0-Upper Row
    "q": (0, 0, 5),
    "w": (0, 0, 4),
    "e": (0, 0, 3),
    "r": (0, 0, 2),
    "t": (0, 0, 1),
    "y": (1, 0, 1),
    "u": (1, 0, 2),
    "i": (1, 0, 3),
    "o": (1, 0, 4),
    "p": (1, 0, 5),
    # 1-Home Row
    "a": (0, 1, 5),
    "s": (0, 1, 4),
    "d": (0, 1, 3),
    "f": (0, 1, 2),
    "g": (0, 1, 1),
    "h": (1, 1, 1),
    "j": (1, 1, 2),
    "k": (1, 1, 3),
    "l": (1, 1, 4),
    # 2-Bottom Row
    "z": (0, 2, 5),
    "x": (0, 2, 4),
    "c": (0, 2, 3),
    "v": (0, 2, 2),
    "b": (0, 2, 1),
    "n": (1, 2, 1),
    "m": (1, 2, 2),
}

ideal_workload_distribution: dict[tuple[int, int, int], float] = {
    # 0-Upper Row
    (0, 0, 5): 1.168,
    (0, 0, 4): 3.170,
    (0, 0, 3): 4.060,
    (0, 0, 2): 2.724,
    (0, 0, 1): 1.835,
    (1, 0, 1): 1.835,
    (1, 0, 2): 2.724,
    (1, 0, 3): 4.060,
    (1, 0, 4): 3.170,
    (1, 0, 5): 1.168,
    # 1-Home Row
    (0, 1, 5): 2.854,
    (0, 1, 4): 7.747,
    (0, 1, 3): 9.922,
    (0, 1, 2): 6.657,
    (0, 1, 1): 4.486,
    (1, 1, 1): 4.486,
    (1, 1, 2): 6.657,
    (1, 1, 3): 9.922,
    (1, 1, 4): 7.747,
    # 2-Bottom Row
    (0, 2, 5): 0.907,
    (0, 2, 4): 2.463,
    (0, 2, 3): 3.155,
    (0, 2, 2): 2.117,
    (0, 2, 1): 1.427,
    (1, 2, 1): 1.427,
    (1, 2, 2): 2.117,
}

single_freqs: dict[str, float] = json.load(open("single_freqs.json", "r"))
pair_freqs: dict[tuple[str, str], float] = {
    tuple(k.split("+")): v for k, v in json.load(open("pair_freqs.json", "r")).items()
}

### Xiaohe Shuangpin (小鹤双拼) configurations

# Map variant finals to standard finals
# standards appear on the top of the key in the keyboard diagram
# variants appear below the standards
xiaohe_variant_to_standard_finals = {
    "ve": "ue",
    "o": "uo",
    "iong": "ong",
    "ing": "uai",
    "iang": "uang",
    "ia": "ua",
    "v": "ui",
}

xiaohe_layout: dict[str, str] = {
    "iu": "q",
    "ei": "w",
    "uan": "r",
    "ue": "t",
    "un": "y",
    "sh": "u",
    "ch": "i",
    "uo": "o",
    "ie": "p",
    "ong": "s",
    "ai": "d",
    "en": "f",
    "eng": "g",
    "ang": "h",
    "an": "j",
    "uai": "k",
    "uang": "l",
    "ou": "z",
    "ua": "x",
    "ao": "c",
    "ui": "v",
    "zh": "v",
    "in": "b",
    "iao": "n",
    "ian": "m",
}

xiaohe_zero_consonant_layout: dict[str, tuple[str, str]] = {
    "a": ("a", "a"),
    "e": ("e", "e"),
    "o": ("o", "o"),
    "ai": ("a", "i"),
    "ei": ("e", "i"),
    "ou": ("o", "u"),
    "an": ("a", "n"),
    "en": ("e", "n"),
    "ang": ("a", "h"),
    "eng": ("e", "g"),
    "ao": ("a", "o"),
    "er": ("e", "r"),
}


def xiaohe_get_standard_component(final: str) -> str:
    return xiaohe_variant_to_standard_finals.get(final, final)


class Choice(Enum):
    LEFT = True
    RIGHT = False


def is_zero_consonant_final(final: str) -> bool:
    return final.endswith("F")


def strip_zero_consonant_final_tag(final: str) -> str:
    return final[:-1]


class Finger(IntEnum):
    INDEX = 0
    MIDDLE = 1
    RING = 2
    LITTLE = 3


def get_finger(key: Key) -> Finger:
    i = qwerty_layout[key][1]
    if i == 1 or i == 2:
        return Finger.INDEX
    elif i == 3:
        return Finger.MIDDLE
    elif i == 4:
        return Finger.RING
    else:
        return Finger.LITTLE


def is_same_finger(i: Key, j: Key) -> bool:
    return get_finger(i) == get_finger(j)


def is_same_hand(i: Key, j: Key) -> bool:
    return qwerty_layout[i][0] == qwerty_layout[j][0]


# Manhattan distance between letter i and letter j
# distance(i, j) = |col(loc(i)) − col(loc(j))| + |row(loc(i)) − row(loc(j))|
def distance(i: Key, j: Key) -> int:
    return abs(qwerty_layout[i][2] - qwerty_layout[j][2]) + abs(
        qwerty_layout[i][1] - qwerty_layout[j][1]
    )


# Preferred hit direction is from little finger to index finger
def is_preferred_hit_direction(i: Key, j: Key) -> bool:
    return get_finger(i) >= get_finger(j)


def xiaohe_get_key(i: str, zero_consonant_choice: Choice) -> str:
    if is_zero_consonant_final(i):
        final = strip_zero_consonant_final_tag(i)
        return xiaohe_zero_consonant_layout[final][
            0 if zero_consonant_choice == Choice.LEFT else 1
        ]
    standard_component = xiaohe_get_standard_component(i)
    return xiaohe_layout.get(standard_component, standard_component)


xiaohe_single_key_freqs: dict[Key, float] = single_freqs.copy()
xiaohe_pair_key_freqs: dict[tuple[Key, Key], float] = pair_freqs.copy()

for standard, variant in xiaohe_variant_to_standard_finals.items():
    xiaohe_single_key_freqs[standard] += xiaohe_single_key_freqs[variant]
    xiaohe_single_key_freqs.pop(variant)

for pair, freq in xiaohe_pair_key_freqs.copy().items():
    standard_pair = (
        xiaohe_get_standard_component(pair[0]),
        xiaohe_get_standard_component(pair[1]),
    )
    if pair != standard_pair:
        variant_freq = xiaohe_pair_key_freqs.pop(pair)
        xiaohe_pair_key_freqs[standard_pair] = (
            xiaohe_pair_key_freqs.get(standard_pair, 0) + variant_freq
        )


def xiaohe_workload_distribution() -> float:
    key_freqs: dict[Key, float] = dict()
    for i, freq in xiaohe_single_key_freqs.items():
        if is_zero_consonant_final(i):
            final = strip_zero_consonant_final_tag(i)
            (first_key, second_key) = xiaohe_zero_consonant_layout[final]
            key_freqs[first_key] = key_freqs.get(first_key, 0) + freq
            key_freqs[second_key] = key_freqs.get(second_key, 0) + freq
        else:
            # The zero consonant choice doesn't matter because we handled it above
            key = xiaohe_get_key(i, Choice.LEFT)
            key_freqs[key] = key_freqs.get(key, 0) + freq
    I1 = 0.0
    for key, freq in key_freqs.items():
        key_location = qwerty_layout[key]
        I1 += ((freq - ideal_workload_distribution[key_location]) / 100) ** 2
    return I1


def xiaohe_hand_alternation() -> float:
    I2 = 0.0
    for (i, j) in xiaohe_pair_key_freqs:
        i_key = xiaohe_get_key(i, Choice.RIGHT)
        j_key = xiaohe_get_key(j, Choice.LEFT)
        if is_same_hand(i_key, j_key):
            # Gives penalty if the two keys are on the same hand
            I2 += xiaohe_pair_key_freqs[(i, j)]
    # add zero-consonant hand alternations
    for final, key_pair in xiaohe_zero_consonant_layout.items():
        if is_same_hand(key_pair[0], key_pair[1]):
            I2 += xiaohe_single_key_freqs.get(final, 0)
    return I2 / 100


def xiaohe_finger_alternation() -> float:
    I3 = 0.0
    for (i, j) in xiaohe_pair_key_freqs:
        i_key = xiaohe_get_key(i, Choice.RIGHT)
        j_key = xiaohe_get_key(j, Choice.LEFT)
        if is_same_hand(i_key, j_key) and is_same_finger(i_key, j_key):
            # Gives penalty if the pair is on the same hand and the same finger
            I3 += xiaohe_pair_key_freqs[(i, j)] * distance(i_key, j_key)
    # add zero-consonant finger alternations
    for final, key_pair in xiaohe_zero_consonant_layout.items():
        if is_same_hand(key_pair[0], key_pair[1]) and is_same_finger(
            key_pair[0], key_pair[1]
        ):
            I3 += xiaohe_single_key_freqs.get(final, 0) * distance(
                key_pair[0], key_pair[1]
            )
    return I3 / 100


penalty_coefficient_for_big_steps: dict[tuple[Finger, Finger], int] = {
    # first finger is index
    (Finger.INDEX, Finger.INDEX): 0,
    (Finger.INDEX, Finger.MIDDLE): 5,
    (Finger.INDEX, Finger.RING): 8,
    (Finger.INDEX, Finger.LITTLE): 6,
    # second finger is middle
    (Finger.MIDDLE, Finger.INDEX): 5,
    (Finger.MIDDLE, Finger.MIDDLE): 0,
    (Finger.MIDDLE, Finger.RING): 9,
    (Finger.MIDDLE, Finger.LITTLE): 7,
    # third finger is ring
    (Finger.RING, Finger.INDEX): 8,
    (Finger.RING, Finger.MIDDLE): 9,
    (Finger.RING, Finger.RING): 0,
    (Finger.RING, Finger.LITTLE): 10,
    # fourth finger is little
    (Finger.LITTLE, Finger.INDEX): 6,
    (Finger.LITTLE, Finger.MIDDLE): 7,
    (Finger.LITTLE, Finger.RING): 10,
    (Finger.LITTLE, Finger.LITTLE): 0,
}


def get_big_step_penalty(i: Key, j: Key) -> int:
    return penalty_coefficient_for_big_steps[(get_finger(i), get_finger(j))]


def xiaohe_big_steps() -> float:
    I4 = 0.0
    for (i, j) in xiaohe_pair_key_freqs:
        i_key = xiaohe_get_key(i, Choice.RIGHT)
        j_key = xiaohe_get_key(j, Choice.LEFT)
        if is_same_hand(i_key, j_key):
            # Gives penalty if the pair is on the same hand
            I4 += xiaohe_pair_key_freqs[(i, j)] * get_big_step_penalty(i_key, j_key)
    # add zero-consonant finger alternations
    for final, key_pair in xiaohe_zero_consonant_layout.items():
        if is_same_hand(key_pair[0], key_pair[1]):
            I4 += xiaohe_single_key_freqs.get(final, 0) * get_big_step_penalty(
                key_pair[0], key_pair[1]
            )
    return I4 / 100


def xiaohe_hit_direction() -> float:
    I5 = 0.0
    for (i, j) in xiaohe_pair_key_freqs:
        i_key = xiaohe_get_key(i, Choice.RIGHT)
        j_key = xiaohe_get_key(j, Choice.LEFT)
        if is_same_hand(i_key, j_key) and not is_preferred_hit_direction(i_key, j_key):
            # Gives penalty if the pair is on the same hand and not in preferred hit direction
            I5 += xiaohe_pair_key_freqs[(i, j)]
    # add zero-consonant finger alternations
    for final, key_pair in xiaohe_zero_consonant_layout.items():
        if is_same_hand(key_pair[0], key_pair[1]) and not is_preferred_hit_direction(
            key_pair[0], key_pair[1]
        ):
            I5 += xiaohe_single_key_freqs.get(final, 0)
    return I5 / 100


def xiaohe_score() -> float:
    return (
        xiaohe_workload_distribution() * 0.45
        + xiaohe_hand_alternation() * 1.0
        + xiaohe_finger_alternation() * 0.8
        + xiaohe_big_steps() * 0.7
        + xiaohe_hit_direction() * 0.6
    )


print(xiaohe_workload_distribution())
print(xiaohe_hand_alternation())
print(xiaohe_finger_alternation())
print(xiaohe_big_steps())
print(xiaohe_hit_direction())

print(xiaohe_score())
