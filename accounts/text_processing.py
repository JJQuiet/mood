import jieba
import csv
import jieba.posseg as posseg
import pandas as pd
import codecs
import collections  # 词频统计库
import wordcloud
from PIL import Image
import numpy as np

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree


# 对csv文件进行中文分词以及去停用词
def delete_stopwords(stopwordfile, filename, outfilename):  # 停用词库;需要处理的文件；处理完后的文件
    # 创建一个停用词列表
    stopwords = [line.strip() for line in open(stopwordfile, encoding='UTF-8').readlines()]
    # 打开要处理的文件
    inputs = open(filename, 'r')
    # 打开保存至文件
    outputs = open(outfilename, 'w')
    for line in inputs:
        # 对文档中的每一行进行中文分词
        sentence_depart = jieba.cut(line.strip())
        outstr = ''
        # 去停用词
        for word in sentence_depart:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        outputs.write(outstr + '\n')
    outputs.close()
    inputs.close()
    return outfilename  # 可返回新生成的文件名


# delete_stopwords('baidu_stopwords.txt','test.txt','result.txt')
# delete_stopwords('baidu_stopwords.txt', 'test.csv', 'result.csv')


# 统计csv文件各词词性
def word_class(filename, column_name):  # 文件，列
    c = collections.Counter()
    with open(filename, 'r')as f:
        reader = csv.reader(f)
        for i in reader:
            segn = posseg.cut(i[column_name], use_paddle=True)
            for word, flag in segn:
                if len(word) >= 1:
                    if word == '\r\n' or word == '\n' or word == ' ' or word == '/' or word == '[' or word == ']' or word == '@' or word == '，' or word == ':' or word == '!' or word == '！' or word == '。':
                        continue
                    else:
                        c[flag] += 1
                # print('%s %s' % (word, flag))
    # print(c)
    list = {}
    i = 0
    n = len(c)
    print('词性统计结果: \n')
    for (k, v) in c.most_common(n):
        list[i] = [k, v]
        i = i + 1
        print('%s%s   %d' % ('  ' * (3), k, v))
    return list


# 统计csv文件词频前n
def word_frequency(filename, n):  # 文件 个数
    test = open(filename, 'r').read()
    words = jieba.lcut(test)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    print(f'词频排名前{n}统计结果：')
    counts = []
    for i in range(n):
        word, count = items[i]
        print("{0:10}{1:>5}".format(word, count))


# 生成词云(文本文件，背景颜色，字体路径，宽度，高度，输出的图片文件，蒙版图片文件)
def word_cloud(filename, bgcolor, font_path, width, height, outfile, maskfile):
    # 蒙版
    usa_mask = np.array(Image.open(maskfile))
    txt = open(filename, 'r').read()
    words = jieba.lcut(txt)  # 精确分词，不会产生冗余
    newtxt = ' '.join(words)  # 空格拼接
    wd = wordcloud.WordCloud(font_path=font_path,
                             width=width,
                             height=height,
                             background_color=bgcolor,
                             mask=usa_mask).generate(newtxt)
    wd.to_file(outfile)
    return outfile


#经过去停用词处理的文件
# file = delete_stopwords('baidu_stopwords.txt', 'test.csv', 'result.csv')
# # 文件词性统计结果
# word_class(file, 1)
# # 文件词频统计结果
# word_frequency(file, 20)
# word_cloud('result.csv', 'black', '/fonts/simhei.ttf', 500, 300, '微博评论词云图.jpg', 'flag.png')


# 句法结构分析(主谓宾、定状补)
def sentence_analyse(sentense):
    # nlp = StanfordCoreNLP('stanford-corenlp-full-2016-10-31',lang='zh')
    nlp = StanfordCoreNLP('stanford-corenlp-full-2016-10-31')
    print('Constituency Parsing:', nlp.parse(sentense))  # 语法树
    nlp.close()  # 释放，否则后端服务器将消耗大量内存

s='张三和李四在2019年3月23日在北京的腾讯技术有限公司一起开会。'
#s = 'At the end of the day, successfully launching a new product means reaching the right audience and consistently delivering a very convincing message. To avoid spending money recklessly because of disjointed strategies, we have developed several recommendations.'
sentence_analyse(s)

def test(text):
    return text