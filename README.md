# Pinyin Frequencies

# Motivations

Knowing the frequencies of Pinyin initials and finals is important for the design of ergonomic Shuangpin input methods. For instance, frequency data can inform the design of the mappings from initials and finals to a key on the keyboard. Frequency data can also help smooth out the learning curve of Shuangpin input methods by progressively introducing mappings one after another, from the most frequently used initials and finals, to the least used. As an example, it may be easier for the typist familiar with standard Pinyin to start by remembering a single mapping from the digraph initial sh to some key rather than being required to memorize all such mappings from the get-go.

# Source

Our source is a corpus of 4.1 million questions and answers from [Zhihu](zhihu.com) collected from the year 2015 to 2016. The total data occupies 3.7G, or 1.7G compressed.

We only included the test and validation data in this repo due to GitHub's file size limit. The training set contains 4.12 million Q&As, the validation set contains 68,000 Q&As, and the testing set A contains 68,000 Q&As.

You can download the train data `web_text_zh_train.json` from [brightmart/nlp_chinese_corpus](https://github.com/brightmart/nlp_chinese_corpus#4%E7%A4%BE%E5%8C%BA%E9%97%AE%E7%AD%94json%E7%89%88webtext2019zh-%E5%A4%A7%E8%A7%84%E6%A8%A1%E9%AB%98%E8%B4%A8%E9%87%8F%E6%95%B0%E6%8D%AE%E9%9B%86).

## Format
```
{
	"qid":<qid>, "title":<title>, "desc":<desc>,
	"topic":<topic>, "star":<star>, "content":<content>,
	"answer_id":<answer_id>, "answerer_tags":<answerer_tags>
}
qid = ID of the question
title = title of the question
desc = description of the question (can be an empty string)
topic = topic the question belongs to
star = number of stars received by that answer
content = content of the answer
answer_id = ID of the answer
answerer_tags = Tags of the answerer
```

For the purpose of this repo, we only care about the fields `title`, `desc`, and `content`.

## Rationale
We chose this Q&A corpus because it represents a mix of colloquial conversations and more formal discussions. Unlike newspapers and Wikipedia, the many answers are written in a style closer to colloquial speech like those seen in chat messages. We think this mix should capture the essential needs of users of Chinese input methods in casual chats, school, and work.

# Results
The following results are computed from `web_text_zh_train.json` with 4.12 million Q&As. A notable observation is that the frequency results already stabilizes at around 68,000 Q&As, ie the testing or validation sets. The result of the testing set A has identical frequency percentage for all initials and finals. The result of the validation set is also identical except that the percentage of the final eng is 1% higher in validation and the extremely rare final m is missing. We suggest you use run the `process_parallel.py` version instead of the serial `process.py` version. Running the parallel version on a 2021 MacBook Pro with M1 Max (64GB RAM and 10 cores), the testing and validation set takes about 17 seconds to complete and the training set takes about 17 minutes. The serial version is much, much slower, taking about 10 minutes and 3 hours respectively.

## Frequencies of initials
Number of initials in the corpus: 940421490
```
Initial Percent Count
d       11      102738722
y       9       89264905
sh      8       78185224
j       6       60251043
x       6       52646568
zh      6       51995442
h       5       49848324
g       5       46427088
l       5       46070010
b       5       45979167
w       4       40501485
m       4       35382204
z       4       33337269
t       3       31506581
q       3       27873173
n       3       27159555
r       3       24011040
ch      2       21577762
f       2       20682451
k       2       19919897
s       1       13306095
p       1       11635248
c       1       10122237
```

## Frequencies of finals
Number of finals in the corpus: 950294801
```
Final   Percent Count
i       17      157093754
e       12      111246835
u       8       74722162
en      5       44380504
an      4       39408484
ou      4       38960226
a       4       38399673
ai      4       38190020
ao      4       35919413
ian     4       33955869
uo      3       32097320
ing     3       28568841
ang     3       28251264
ong     3       28084595
ei      3       27845158
eng     2       23746910
ui      2       18714415
uan     2       18220972
o       2       17024398
in      2       15766724
ie      2       14533166
iao     1       13564920
iang    1       13229423
ue      1       11721619
iu      1       11152123
ia      1       10103918
un      1       7188177
ua      0       4556329
er      0       4252925
uang    0       3887608
v       0       3070058
uai     0       1670704
iong    0       529863
ve      0       236428
m       0       3
```