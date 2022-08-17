from shuangpin import ShuangpinConfig

### Foxi Shuangpin (佛系双拼) configurations
config = ShuangpinConfig(
    final_layout={
        "iu": "q",
        "in": "w",
        "un": "r",
        "ua": "t",
        "ong": "y",
        "uo": "o",
        "ang": "p",
        "uai": "s",
        "ao": "d",
        "ou": "f",
        "uan": "g",
        "eng": "h",
        "ian": "j",
        "an": "k",
        "ai": "l",
        "iao": "z",
        "ue": "x",
        "uang": "c",
        "ui": "v",
        "ie": "b",
        "ei": "n",
        "en": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "e",
        "ch": "a",
        "sh": "v",
    },
    zero_consonant_final_layout={
        "a": ("a", "k"),
        "e": ("e", "k"),
        "o": ("o", "s"),
        "ai": ("a", "i"),
        "ei": ("e", "i"),
        "ou": ("o", "u"),
        "an": ("a", "n"),
        "en": ("e", "n"),
        "ang": ("a", "j"),
        # Generated config is ("e", "o")
        # but since "eng" practically never occurs in the corpus
        # this is a random assignment
        # we changed the layout to align with ang
        "eng": ("e", "j"),
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
