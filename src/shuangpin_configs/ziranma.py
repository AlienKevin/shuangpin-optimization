from shuangpin import ShuangpinConfig

### Ziranma (自然码) configurations
config = ShuangpinConfig(
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
