import re
import time
from models import InferSent
import sys
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from nltk.stem.lancaster import LancasterStemmer
from nltk import Tree
import spacy
import numpy as np
import pandas as pd
import json
import ast
from textblob import TextBlob
import nltk
import torch
import pickle
from scipy import spatial
import warnings
warnings.filterwarnings('ignore')
en_nlp = spacy.load('en')
st = LancasterStemmer()

nltk.download('punkt')

train_set = "/content/gdrive/MyDrive/SQUAD_Tuning/train-v2.0.json"
train = pd.read_json(train_set)

amazon = "/content/gdrive/MyDrive/SQUAD_Tuning/qar-squad.json"
amazonqa = pd.read_json(amazon, lines=True)

df = pd.DataFrame()
contexts = amazonqa['context']
versions = []
data = []
for i in range(len(contexts)):
    lst = []
    paragraphs = []
    samp_dict = {}
    answers = []
    samp = amazonqa['qas'][i]
    sample = samp[0]
    answer = sample['answers_sentence_bleu2'][0]
    answers.append(answer)
    samp_dict['answers'] = answers
    samp_dict['id'] = '2t523njt3t'
    samp_dict['is_impossible'] = sample['is_impossible']
    samp_dict['question'] = sample['question']
    lst.append(samp_dict)
    context = amazonqa['context'][i]
    paradict = {}
    paradict['context'] = context
    paradict['qas'] = lst
    paragraphs.append(paradict)
    para = {}
    para['paragraphs'] = paragraphs
    para['title'] = "Review"
    versions.append("v2.0")
    data.append(para)
df['version'] = versions
df['data'] = data

xy = pd.concat([train, df], axis=0)

contexts = []
questions = []
answers_text = []
answers_start = []
for i in range(xy.shape[0]):
    # print(i)
    topic = xy.iloc[i, 1]['paragraphs']
    for sub_para in topic:
        for q_a in sub_para['qas']:
            questions.append(q_a['question'])
            # print(q_a['answers'])
            if len(q_a['answers']) > 0:
                answers_start.append(q_a['answers'][0]['answer_start'])
                answers_text.append(q_a['answers'][0]['text'])
            else:
                answers_start.append(0)
                answers_text.append('N/A')
            contexts.append(sub_para['context'])
df = pd.DataFrame({"context": contexts, "question": questions,
                  "answer_start": answers_start, "text": answers_text})


sys.path.insert(0, '/content/gdrive/MyDrive/SQUAD_Tuning/InferSent')


V = 2
MODEL_PATH = '/content/gdrive/MyDrive/SQUAD_Tuning/InferSent/infersent%s.pkl' % V
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': V}
model = InferSent(params_model)
model.load_state_dict(torch.load(
    MODEL_PATH, map_location=lambda storage, loc: storage))
W2V_PATH = '/content/gdrive/MyDrive/SQUAD_Tuning/InferSent/glove.840B.300d.txt'
model.set_w2v_path(W2V_PATH)

infersent = model
infersent.build_vocab(paras, tokenize=True)
model = infersent


alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms+" "+starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" +
                  alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets +
                  "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" "+suffixes+"[.] "+starters, " \\1<stop> \\2", text)
    text = re.sub(" "+suffixes+"[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if "?" in text:
        text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def answer_question(question, context):
    # Split Context into individual sentences
    start = time.time()
    sentences = split_into_sentences(context)

    # model.build_vocab(sentences, tokenize=True)
    query_vec = model.encode(question)[0]

    similarity = []
    for sent in sentences:
        sim = cosine(query_vec, model.encode([sent])[0])
        similarity.append(sim)
        # print("Sentence = ", sent, "; similarity = ", sim)

    n_similarity = np.array(similarity)
    max_index = np.argmax(n_similarity, axis=0)

    answer = sentences[max_index]
    end = time.time()
    print("INFERENCE TIME: ", end - start)
    return answer


def question_answer(question, reviews_text):

    return "Unsupervised Answer"
