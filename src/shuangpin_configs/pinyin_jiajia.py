from shuangpin import ShuangpinConfig

### Pinyin Jiajia (拼音加加) configurations
config = ShuangpinConfig(
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
