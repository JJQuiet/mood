from stanfordcorenlp import StanfordCoreNLP
import os
from django.conf import settings

# from django.conf.settings import BASE_DIR
from mood.settings import BASE_DIR
def word_tokenize(sentence):
    # with StanfordCoreNLP(r'D:\aa\IT\Python\Django\a-mood\a-sentic-1-1\stanford-corenlp', lang='zh') as nlp:
    # nlp = StanfordCoreNLP(r'D:\aa\IT\Python\Django\a-mood\a-sentic-1-1\stanford-corenlp', lang='zh')
    nlp = StanfordCoreNLP(os.path.join(BASE_DIR, 'stanford-corenlp'), lang='zh')
    # print(nlp.pos_tag(sentence))
    # print(nlp.ner(sentence))
    # print(nlp.parse(sentence))
    # print(nlp.dependency_parse(sentence))
    result = nlp.word_tokenize(sentence)
    # print(result)
    nlp.close()
    return result


def stanfordCoreNLP_process(sentence):
    # with StanfordCoreNLP(r'D:\aa\IT\Python\Django\a-mood\a-sentic-1-1\stanford-corenlp', lang='zh') as nlp:
    # nlp = StanfordCoreNLP(r'D:\aa\IT\Python\Django\a-mood\a-sentic-1-1\stanford-corenlp', lang='zh')
    nlp = StanfordCoreNLP(os.path.join(BASE_DIR, 'stanford-corenlp'), lang='zh')
    result = {}
    result['word_tokenize'] = nlp.word_tokenize(sentence)
    result['pos_tag'] = nlp.pos_tag(sentence)
    result['ner'] = nlp.ner(sentence)
    result['parse'] = nlp.parse(sentence)
    result['dependency_parse'] = nlp.dependency_parse(sentence)
    # print(nlp.pos_tag(sentence))
    # print(nlp.ner(sentence))
    # print(nlp.parse(sentence))
    # print(nlp.dependency_parse(sentence))
    nlp.close()
    return result
