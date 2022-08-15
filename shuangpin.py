import json
from enum import Enum, IntEnum
from dataclasses import dataclass
import random
from itertools import product

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


@dataclass
class ShuangpinConfig:
    # Maps standard finals to keys
    final_layout: dict[str, str]
    # digraph initials' keys must be unique among all digraph initials
    # but they can share the keys with finals
    digraph_initial_layout: dict[str, str]
    zero_consonant_final_layout: dict[str, tuple[str, str]]
    # Map variant finals to standard finals
    # REQUIRES: the standard final values must be unique
    variant_to_standard_finals: dict[str, str]


digraph_initials: list[str] = ["zh", "ch", "sh"]


def is_digraph_initial(initial: str) -> bool:
    return initial in digraph_initials


### Xiaohe Shuangpin (小鹤双拼) configurations
xiaohe_config = ShuangpinConfig(
    final_layout={
        "iu": "q",
        "ei": "w",
        "uan": "r",
        "ue": "t",
        "un": "y",
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
        "in": "b",
        "iao": "n",
        "ian": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "v",
        "ch": "i",
        "sh": "u",
    },
    zero_consonant_final_layout={
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
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        "ve": "ue",
        "o": "uo",
        "iong": "ong",
        "ing": "uai",
        "iang": "uang",
        "ia": "ua",
        "v": "ui",
    },
)

### Foxi Shuangpin (佛系双拼) configurations
foxi_config = ShuangpinConfig(
    final_layout={
        "iu": "q",
        "ei": "w",
        "un": "r",
        "ua": "t",
        "ang": "y",
        "uo": "o",
        "ong": "p",
        "iao": "s",
        "ue": "d",
        "ou": "f",
        "uan": "g",
        "eng": "h",
        "ian": "j",
        "an": "k",
        "ai": "l",
        "in": "z",
        "ie": "x",
        "ao": "c",
        "ui": "v",
        "uai": "b",
        "uang": "n",
        "en": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "e",
        "ch": "a",
        "sh": "v",
    },
    zero_consonant_final_layout={
        "a": ("a", "j"),
        "e": ("e", "j"),
        "o": ("o", "f"),
        "ai": ("a", "i"),
        "ei": ("e", "i"),
        "ou": ("o", "u"),
        "an": ("a", "n"),
        "en": ("e", "n"),
        "ang": ("a", "h"),
        "eng": ("e", "h"),
        "ao": ("a", "o"),
        "er": ("e", "r"),
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        "ve": "ue",
        "o": "uo",
        "iong": "ong",
        "ing": "uai",
        "iang": "uang",
        "ia": "ua",
        "v": "ui",
    },
)


### Ziranma (自然码) configurations
ziranma_config = ShuangpinConfig(
    final_layout={
        "iu": "q",
        "ua": "w",
        "uan": "r",
        "ue": "t",
        "uai": "y",
        "uo": "o",
        "un": "p",
        "ong": "s",
        "uang": "d",
        "en": "f",
        "eng": "g",
        "ang": "h",
        "an": "j",
        "ao": "k",
        "ai": "l",
        "ei": "z",
        "ie": "x",
        "iao": "c",
        "ui": "v",
        "ou": "b",
        "in": "n",
        "ian": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "v",
        "ch": "i",
        "sh": "u",
    },
    zero_consonant_final_layout={
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
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        "ve": "ue",
        "o": "uo",
        "iong": "ong",
        "ing": "uai",
        "iang": "uang",
        "ia": "ua",
        "v": "ui",
    },
)


### Intelligent ABC (智能ABC) configurations
intelligent_abc_config = ShuangpinConfig(
    final_layout={
        "ei": "q",
        "ian": "w",
        "iu": "r",
        "uang": "t",
        "ing": "y",
        "uo": "o",
        "uan": "p",
        "ong": "s",
        "ua": "d",
        "en": "f",
        "eng": "g",
        "ang": "h",
        "an": "j",
        "ao": "k",
        "ai": "l",
        "iao": "z",
        "ie": "x",
        "uai": "c",
        "ve": "v",
        "ou": "b",
        "un": "n",
        "ui": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "a",
        "ch": "e",
        "sh": "v",
    },
    zero_consonant_final_layout={
        "a": ("o", "a"),
        "e": ("o", "e"),
        "o": ("o", "o"),
        "ai": ("o", "l"),
        "ei": ("o", "q"),
        "ou": ("o", "b"),
        "an": ("o", "j"),
        "en": ("o", "f"),
        "ang": ("o", "h"),
        "eng": ("o", "g"),
        "ao": ("o", "k"),
        "er": ("o", "r"),
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        # "er": "iu", # er can only appear as a zero-consonant final
        "iang": "uang",
        "o": "uo",
        "iong": "ong",
        "ia": "ua",
        "in": "uai",
        "v": "ve",
        "ue": "ui",
    },
)


### Pinyin Jiajia (拼音加加) configurations
pinyin_jiajia_config = ShuangpinConfig(
    final_layout={
        "ing": "q",
        "ei": "w",
        "en": "r",
        "eng": "t",
        "ong": "y",
        "uo": "o",
        "ou": "p",
        "ai": "s",
        "ao": "d",
        "an": "f",
        "ang": "g",
        "uang": "h",
        "ian": "j",
        "iao": "k",
        "in": "l",
        "un": "z",
        "uai": "x",
        "uan": "c",
        "ui": "v",
        "ua": "b",
        "iu": "n",
        "ie": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "v",
        "ch": "u",
        "sh": "i",
    },
    zero_consonant_final_layout={
        "a": ("a", "a"),
        "e": ("e", "e"),
        "o": ("o", "o"),
        "ai": ("a", "s"),
        "ei": ("e", "w"),
        "ou": ("o", "p"),
        "an": ("a", "f"),
        "en": ("e", "r"),
        "ang": ("a", "g"),
        "eng": ("e", "t"),
        "ao": ("a", "d"),
        "er": ("e", "q"),
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        # "er": "ing", # er can only appear as a zero-consonant final
        "iong": "ong",
        "o": "uo",
        "iang": "uang",
        "ue": "uai",
        # ve seems to be implicitly combined with ue
        # see https://www.zhihu.com/question/342959519/answer/1336034357
        "ve": "uai",
        "v": "ui",
        "ia": "ua",
    },
)


def get_fixed_final_keys(
    final_layout: dict[str, str], variant_to_standard_finals: dict[str, str]
) -> set[Key]:
    standard_to_variant_finals = {v: k for k, v in variant_to_standard_finals.items()}
    fixed_final_keys = set()
    for final, key in final_layout.items():
        if final == key or standard_to_variant_finals.get(final) == key:
            fixed_final_keys.add(key)
    return fixed_final_keys


def get_random_final_layout(
    final_layout: dict[str, str], variant_to_standard_finals: dict[str, str]
) -> dict[str, str]:
    fixed_final_keys = get_fixed_final_keys(final_layout, variant_to_standard_finals)
    flexible_final_keys = set(final_layout.values()) - fixed_final_keys
    random_layout = dict()
    for final, key in final_layout.items():
        if key in fixed_final_keys:
            random_layout[final] = key
        else:
            random_layout[final] = random.choice(list(flexible_final_keys))
            flexible_final_keys.remove(random_layout[final])
    return random_layout


# print(
#     get_random_final_layout(
#         xiaohe_config.final_layout, xiaohe_config.digraph_initial_layout
#     )
# )


def get_random_digraph_initial_layout() -> dict[str, str]:
    random_layout = dict()
    flexible_digraph_initial_keys = {"a", "e", "i", "o", "u", "v"}
    for initial in digraph_initials:
        random_layout[initial] = random.choice(list(flexible_digraph_initial_keys))
        flexible_digraph_initial_keys.remove(random_layout[initial])
    return random_layout


# print(get_random_digraph_initial_layout())


def get_random_zero_consonant_final_layout(
    zero_consonant_final_layout: dict[str, tuple[str, str]]
) -> dict[str, tuple[str, str]]:
    random_layout = dict()
    flexible_zero_consonant_finals = {"a", "e", "o", "ang", "eng"}
    flexible_first_keys = {"a", "e", "o"}
    fixed_keys = {
        key
        for final, key in zero_consonant_final_layout.items()
        if final not in flexible_zero_consonant_finals
    }
    flexible_keys: dict[str, set[tuple[str, str]]] = {
        k: (set(product({k}, qwerty_layout.keys())) - fixed_keys)
        for k in flexible_first_keys
    }
    for final in zero_consonant_final_layout.keys():
        if final in flexible_zero_consonant_finals:
            # first key is restricted to the first letter of the final
            first_key = final[0]
            random_layout[final] = random.choice(list(flexible_keys[first_key]))
            flexible_keys[first_key].remove(random_layout[final])
        else:
            random_layout[final] = zero_consonant_final_layout[final]
    return random_layout


# print(get_random_zero_consonant_final_layout(xiaohe_config.zero_consonant_final_layout))


def get_random_config() -> ShuangpinConfig:
    return ShuangpinConfig(
        final_layout=get_random_final_layout(
            xiaohe_config.final_layout, xiaohe_config.variant_to_standard_finals
        ),
        digraph_initial_layout=get_random_digraph_initial_layout(),
        zero_consonant_final_layout=get_random_zero_consonant_final_layout(
            xiaohe_config.zero_consonant_final_layout
        ),
        variant_to_standard_finals=xiaohe_config.variant_to_standard_finals,
    )


def get_score(
    config: ShuangpinConfig,
) -> float:
    def get_standard_final(final: str) -> str:
        return config.variant_to_standard_finals.get(final, final)

    def get_key(i: str, zero_consonant_choice: Choice) -> str:
        if is_zero_consonant_final(i):
            final = strip_zero_consonant_final_tag(i)
            return config.zero_consonant_final_layout[final][
                0 if zero_consonant_choice == Choice.LEFT else 1
            ]
        elif is_digraph_initial(i):
            return config.digraph_initial_layout[i]
        else:
            standard_final = get_standard_final(i)
            return config.final_layout.get(standard_final, standard_final)

    single_key_freqs: dict[Key, float] = single_freqs.copy()
    pair_key_freqs: dict[tuple[Key, Key], float] = pair_freqs.copy()

    for variant, standard in config.variant_to_standard_finals.items():
        single_key_freqs[standard] += single_key_freqs[variant]
        single_key_freqs.pop(variant)

    for pair in pair_key_freqs.copy():
        standard_pair = (
            get_standard_final(pair[0]),
            get_standard_final(pair[1]),
        )
        if pair != standard_pair:
            variant_freq = pair_key_freqs.pop(pair)
            pair_key_freqs[standard_pair] = (
                pair_key_freqs.get(standard_pair, 0) + variant_freq
            )

    def workload_distribution() -> float:
        key_freqs: dict[Key, float] = dict()
        for i, freq in single_key_freqs.items():
            if is_zero_consonant_final(i):
                final = strip_zero_consonant_final_tag(i)
                (first_key, second_key) = config.zero_consonant_final_layout[final]
                key_freqs[first_key] = key_freqs.get(first_key, 0) + freq
                key_freqs[second_key] = key_freqs.get(second_key, 0) + freq
            else:
                # The zero consonant choice doesn't matter because we handled it above
                key = get_key(i, Choice.LEFT)
                key_freqs[key] = key_freqs.get(key, 0) + freq
        I1 = 0.0
        for key, freq in key_freqs.items():
            key_location = qwerty_layout[key]
            I1 += ((freq - ideal_workload_distribution[key_location]) / 100) ** 2
        return I1

    def hand_alternation() -> float:
        I2 = 0.0
        for (i, j) in pair_key_freqs:
            i_key = get_key(i, Choice.RIGHT)
            j_key = get_key(j, Choice.LEFT)
            if is_same_hand(i_key, j_key):
                # Gives penalty if the two keys are on the same hand
                I2 += pair_key_freqs[(i, j)]
        # add zero-consonant hand alternations
        for final, key_pair in config.zero_consonant_final_layout.items():
            if is_same_hand(key_pair[0], key_pair[1]):
                I2 += single_key_freqs.get(final, 0)
        return I2 / 100

    def finger_alternation() -> float:
        I3 = 0.0
        for (i, j) in pair_key_freqs:
            i_key = get_key(i, Choice.RIGHT)
            j_key = get_key(j, Choice.LEFT)
            if is_same_hand(i_key, j_key) and is_same_finger(i_key, j_key):
                # Gives penalty if the pair is on the same hand and the same finger
                I3 += pair_key_freqs[(i, j)] * distance(i_key, j_key)
        # add zero-consonant finger alternations
        for final, key_pair in config.zero_consonant_final_layout.items():
            if is_same_hand(key_pair[0], key_pair[1]) and is_same_finger(
                key_pair[0], key_pair[1]
            ):
                I3 += single_key_freqs.get(final, 0) * distance(
                    key_pair[0], key_pair[1]
                )
        return I3 / 100

    def big_steps() -> float:
        I4 = 0.0
        for (i, j) in pair_key_freqs:
            i_key = get_key(i, Choice.RIGHT)
            j_key = get_key(j, Choice.LEFT)
            if is_same_hand(i_key, j_key):
                # Gives penalty if the pair is on the same hand
                I4 += pair_key_freqs[(i, j)] * get_big_step_penalty(i_key, j_key)
        # add zero-consonant finger alternations
        for final, key_pair in config.zero_consonant_final_layout.items():
            if is_same_hand(key_pair[0], key_pair[1]):
                I4 += single_key_freqs.get(final, 0) * get_big_step_penalty(
                    key_pair[0], key_pair[1]
                )
        return I4 / 100

    def hit_direction() -> float:
        I5 = 0.0
        for (i, j) in pair_key_freqs:
            i_key = get_key(i, Choice.RIGHT)
            j_key = get_key(j, Choice.LEFT)
            if is_same_hand(i_key, j_key) and not is_preferred_hit_direction(
                i_key, j_key
            ):
                # Gives penalty if the pair is on the same hand and not in preferred hit direction
                I5 += pair_key_freqs[(i, j)]
        # add zero-consonant finger alternations
        for final, key_pair in config.zero_consonant_final_layout.items():
            if is_same_hand(
                key_pair[0], key_pair[1]
            ) and not is_preferred_hit_direction(key_pair[0], key_pair[1]):
                I5 += single_key_freqs.get(final, 0)
        return I5 / 100

    return (
        workload_distribution() * 0.45
        + hand_alternation() * 1.0
        + finger_alternation() * 0.8
        + big_steps() * 0.7
        + hit_direction() * 0.6
    )


# print("xiaohe score = {}".format(get_score(xiaohe_config)))
# print("ziranma score = {}".format(get_score(ziranma_config)))
# print("intelligent ABC score = {}".format(get_score(intelligent_abc_config)))
# print("pinyin jiajia score = {}".format(get_score(pinyin_jiajia_config)))
# print("foxi score = {}".format(get_score(foxi_config)))
