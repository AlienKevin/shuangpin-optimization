from shuangpin import ShuangpinConfig

### Foxi Shuangpin (佛系双拼) configurations
config = ShuangpinConfig(
    final_layout={
        "iu": "q",
        "in": "w",
        "ei": "r",
        "un": "t",
        "ong": "y",
        "uo": "o",
        "ang": "p",
        "uai": "s",
        "uan": "d",
        "ou": "f",
        "ua": "g",  # n + g is not a valid combination
        "ian": "h",
        "ao": "j",
        "an": "k",
        "ai": "l",
        "uang": "z",
        "iao": "x",
        "ue": "c",
        "ui": "v",
        "ie": "b",
        "eng": "n",
        "en": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "v",
        "ch": "i",
        "sh": "u",
    },
    zero_consonant_final_layout={
        "a": ("o", "a"),
        "e": ("o", "e"),
        "o": ("o", "o"),
        "ai": ("o", "l"),
        "ei": ("o", "r"),
        "ou": ("o", "f"),
        "an": ("o", "k"),
        "en": ("o", "m"),
        "ang": ("o", "p"),
        "eng": ("o", "n"),
        "ao": ("o", "j"),
        "er": ("o", "d"),
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
