from wordcloud import WordCloud
import matplotlib.pyplot as plt
from .models import Docitems
from snownlp import SnowNLP
from stanfordcorenlp import StanfordCoreNLP
import jieba
import os
from mood.settings import BASE_DIR
def csvreview_file_wordcloud(docID):
    rows = Docitems.objects.filter(document__id=docID)
    review_words = ''
    # custom_stopwords = set(open(os.path.join(BASE_DIR, 'accounts\static\snippets\\baidu_stopwords_custom'), 'r', encoding='UTF-8', errors='ignore').read().splitlines())
    custom_stopwords = open(os.path.join(BASE_DIR, 'accounts\static\snippets\\baidu_stopwords_custom'), 'r', encoding='UTF-8', errors='ignore').read().split("\n") # list [] , object list {} 都可以
    for row in rows:
        text = SnowNLP(row.review)
        review_words += ' '.join(text.words) + ' '
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color = 'white',
                    stopwords = custom_stopwords,
                    min_font_size = 10).generate(review_words)
    plt.figure(figsize = (6, 6), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()


def simple_text_wordcloud(sentence):
    text = jieba.lcut(sentence)
    text = [word for word in text if len(word) > 1]
    text_ = SnowNLP(sentence)
    review_words = ' '.join(text)
    stopwords = open(os.path.join(BASE_DIR, 'accounts\static\snippets\\baidu_stopwords_custom'), 'r', encoding='UTF-8', errors='ignore').read().split("\n")
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color = 'white',
                    stopwords = stopwords,
                    min_font_size = 10).generate(review_words)
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()

    
def stanfordCoreNLP_process(sentence):
    # with StanfordCoreNLP(os.path.join(BASE_DIR, 'stanford-corenlp'), lang='zh') as nlp:
    nlp = StanfordCoreNLP(os.path.join(BASE_DIR, 'stanford-corenlp'), lang='zh')
    result = {}
    result['word_tokenize'] = nlp.word_tokenize(sentence)
    result['pos_tag'] = nlp.pos_tag(sentence)
    result['ner'] = nlp.ner(sentence)
    result['parse'] = nlp.parse(sentence)
    result['dependency_parse'] = nlp.dependency_parse(sentence)
    nlp.close()
    return result
    