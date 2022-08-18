# only_jqx_group can only be paired with no_jqx_group

only_jqx_final = "iong"

no_jqx_group = {
    "a",
    # o must be paired with uo
    # see uo for an explanation
    # "o",
    "e",
    "ai",
    "ei",
    "ao",
    "ou",
    "an",
    "en",
    "ang",
    "eng",
    "ong",
    # the finals below also can't be paired with bpmf
    # can't pair with iong because then iong cannot pair with other finals
    # "ua",
    # uo must be paired with o
    # San Duanmu: I have heard both [o] and [ɤ] after labials, such as [phwo] and [phɤ] for
    # ‘slope’; it is especially common to use [ɤ] after labials in north east China.
    # See Phonology of Standard Chinese, 2nd edition by San Duanmu pg 38
    # For many SC speakers, the mid vowel is [oː] in an open syllable after the
    # labials [p, ph, m, f], where the labials become rounded, too.
    # See Phonology of Standard Chinese, 2nd edition by San Duanmu pg 69
    # "uo",
    # can't pair with iong because then iong cannot pair with other finals
    # "uai",
    # ui must be paired with v
    # See no_jqx_nl_group and only_jqx_group for an explanation
    # "ui",
    # The below two finals can be abbreviations of van and vn respectively.
    # van and vn can be paired with jqx
    # "uan",
    # "un",
    # can't pair with iong because then iong cannot pair with other finals
    # "uang",
}

# only_jqx_nl_group can only be paired with no_jqx_nl_group

only_jqx_nl_group = {
    "v",
    # ve must be paired with ue
    # some people abbreviate lve as lue and nve as nue
    # "ve",
}

no_jqx_nl_group = {
    "ui",
    # only_gkh_group can't be paired with v
    # because then v cannot pair with other finals
    # "ua",
    # "uai",
    # "uang",
}

# only_gkh_group can only be paired with no_gkh_group

only_gkh_group = {
    "ua",
    "uai",
    "uang",  # ignoring the duang neologism
}

no_gkh_group = {
    "i",
    "ia",
    "ie",
    "iao",
    "iu",  # ignoring the kiu 'Q' neologism
    "ian",
    "in",
    "iang",
    "ing",
    # can't pair with only_gkh_group because then only_gkh_group cannot pair with other finals
    # "iong",
    # v must be paired with ui
    # "v",
    # ve must be paired with ue
    # "ve",
}
