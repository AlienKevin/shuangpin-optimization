from shuangpin import get_score
from shuangpin_configs import (
    xiaohe,
    ziranma,
    intelligent_abc,
    pinyin_jiajia,
    guobiao,
    foxi,
)


def print_comparison():
    print("xiaohe score = {}".format(get_score(xiaohe.config)))
    print("ziranma score = {}".format(get_score(ziranma.config)))
    print("intelligent ABC score = {}".format(get_score(intelligent_abc.config)))
    print("pinyin jiajia score = {}".format(get_score(pinyin_jiajia.config)))
    print("guobiao score = {}".format(get_score(guobiao.config)))
    print("foxi score = {}".format(get_score(foxi.config)))


print_comparison()
