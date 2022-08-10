import json
import re
from pypinyin import lazy_pinyin

initial_regex = re.compile(
    "(ch|zh|sh|r|c|b|d|g|f|h|k|j|m|l|n|q|p|s|t|w|y|x|z)")

initial_freq = dict()
final_freq = dict()

with open('web_text_zh_small.json') as f:
    for line in f:
        data = json.loads(line)
        pinyins = lazy_pinyin(data['title'], errors='ignore') + \
            lazy_pinyin(data['desc'], errors='ignore') + \
            lazy_pinyin(data['content'], errors='ignore')
        for pinyin in pinyins:
            match_result = initial_regex.match(pinyin)
            if match_result:
                initial = match_result.groups()[0]
                final = pinyin[len(initial):]
                initial_freq[initial] = initial_freq.get(initial, 0) + 1
                if len(final) > 0:
                    final_freq[final] = final_freq.get(final, 0) + 1
            else:
                final_freq[pinyin] = final_freq.get(pinyin, 0) + 1


def print_freq(label, freq):
    total_count = sum(freq.values())
    print("# of {}: {}".format(label, total_count))
    print(label + '\t' + '%\t' + '#')
    for (key, count) in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        print(key + '\t' + '{:.0f}'.format(count /
              total_count * 100) + '\t' + str(count))
    print()


print_freq("initial", initial_freq)
print_freq("final", final_freq)
