from shuangpin import ShuangpinConfig

### Intelligent ABC (智能ABC) configurations
config = ShuangpinConfig(
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
