from shuangpin import get_score
from shuangpin_configs import (
    xiaohe,
    ziranma,
    intelligent_abc,
    pinyin_jiajia,
    guobiao,
    foxi_1,
    foxi_2,
    foxi_3,
    foxi_4,
    foxi_5,
)


def print_comparison():
    print("xiaohe score = {}".format(get_score(xiaohe.config)))
    print("ziranma score = {}".format(get_score(ziranma.config)))
    print("intelligent ABC score = {}".format(get_score(intelligent_abc.config)))
    print("pinyin jiajia score = {}".format(get_score(pinyin_jiajia.config)))
    print("guobiao score = {}".format(get_score(guobiao.config)))
    print("foxi 1 score = {}".format(get_score(foxi_1.config)))
    print("foxi 2 score = {}".format(get_score(foxi_2.config)))
    print("foxi 3 score = {}".format(get_score(foxi_3.config)))
    print("foxi 4 score = {}".format(get_score(foxi_4.config)))
    print("foxi 5 score = {}".format(get_score(foxi_5.config)))


print_comparison()
