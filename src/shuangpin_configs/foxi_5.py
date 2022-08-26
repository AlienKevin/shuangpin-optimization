from shuangpin import ShuangpinConfig

### Foxi Shuangpin (佛系双拼) configurations
# un	ei	e	in	iu	ong	u	i	uo	ang
# a	ing	iang	ou	ia	ian	ao	an	ai
# ue	ie	uan	ui	iao	eng	en

# zh:e	ch:a	sh:v

# a:ak	e:ek	o:os	ang:al	eng:eu	ai:ai	ei:ei	ou:ou	an:an	en:en	ao:ao	er:er

# ve:ue	o:uo	v:ui	iong:an	ua:ing	uai:iang	uang:ian

config = ShuangpinConfig(
    final_layout={
        "un": "q",
        "ei": "w",
        "in": "r",
        "iu": "t",
        "ong": "y",
        "uo": "o",
        "ang": "p",
        "ua": "s",
        "uai": "d",
        "ou": "f",
        "ia": "g",  # n + g is not a valid combination
        "uang": "h",
        "ao": "j",
        "an": "k",
        "ai": "l",
        "ue": "z",
        "ie": "x",
        "uan": "c",
        "ui": "v",
        "iao": "b",
        "eng": "n",
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
        "ang": ("a", "l"),
        # Generated config is ("e", "u")
        # but since "eng" practically never occurs in the corpus
        # this is a random assignment
        # we changed the layout to align with ang
        "eng": ("e", "l"),
        "ao": ("a", "o"),
        "er": ("e", "r"),
    },
    # standards appear on the top of the key in the keyboard diagram
    # variants appear below the standards
    variant_to_standard_finals={
        "ve": "ue",
        "o": "uo",
        "iong": "an",
        "ing": "ua",
        "iang": "uai",
        "ian": "uang",
        "v": "ui",
    },
)
