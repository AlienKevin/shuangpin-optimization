from shuangpin import ShuangpinConfig

### Guobiao Shuangpin (国标双拼) configurations
config = ShuangpinConfig(
    final_layout={
        "ua": "q",
        "uan": "w",
        "en": "r",
        "ie": "t",
        "uai": "y",
        "uo": "o",
        "ou": "p",
        "ong": "s",
        "ian": "d",
        "an": "f",
        "ang": "g",
        "eng": "h",
        "ing": "j",
        "ai": "k",
        "in": "l",
        "un": "z",
        "ue": "x",
        "ao": "c",
        "ui": "v",
        "ei": "b",
        "uang": "n",
        "iao": "m",
    },
    # keys must be in the order of the digraph_initials list
    digraph_initial_layout={
        "zh": "v",
        "ch": "i",
        "sh": "u",
    },
    zero_consonant_final_layout={
        "a": ("a", "a"),
        "e": ("a", "e"),
        "o": ("a", "o"),
        "ai": ("a", "k"),
        "ei": ("a", "b"),
        "ou": ("a", "p"),
        "an": ("a", "f"),
        "en": ("a", "r"),
        "ang": ("a", "g"),
        "eng": ("a", "h"),
        "ao": ("a", "c"),
        "er": ("a", "l"),
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        "ia": "ua",
        # van (corresponding to üan in Pinyin) is always abbreviated as uan
        # when combined with an initial consonant
        # "van": "uan",
        "iu": "uai",
        "o": "uo",
        "iong": "ong",
        # er can only appear as a zero-consonant final
        # "er": "in",
        # vn (corresponding to ün in Pinyin) is always abbreviated as un
        # when combined with an initial consonant
        # "vn": "un",
        "ve": "ue",
        "v": "ui",
        "iang": "uang",
    },
)
