from syntok.segmenter import segment
from syntok.tokenizer import Tokenizer
import numpy as np

# 1) Tách câu (fallback: syntok). Nếu văn bản đã có câu rõ, bạn có thể regex:
def sentences_from_text(text):
    # syntok: đoạn -> câu
    sents = []
    tokenizer = Tokenizer()
    for para in text.split('\n'):
        # Tokenize and then segment each paragraph
        for sent in segment(tokenizer.tokenize(para)):
            print(sent)
            s = "".join(tok.spacing + tok.value for tok in sent).strip()
            if s: sents.append(s)
    return sents


def calculate_novalty(embedded_sentences, w=15):
    # 3) Novelty score
    # w = 15  # thử 5–10
    L = np.array([embedded_sentences[max(0,i-w):i].mean(axis=0) for i in range(len(embedded_sentences))])
    R = np.array([embedded_sentences[i:min(len(embedded_sentences),i+w)].mean(axis=0) for i in range(len(embedded_sentences))])
    # tránh NaN ở biên
    L[~np.isfinite(L)] = 0; R[~np.isfinite(R)] = 0
    novelty = 1 - (L * R).sum(axis=1)  # cosine vì vector đã chuẩn hóa
    return novelty


def normalize_novelty(novelty):
    # Normalize novelty score (Min-Max scaling)
    return (novelty - np.min(novelty)) / (np.max(novelty) - np.min(novelty))


def moving_average(novelty, k=50):
    # 4) Làm trơn (moving average)
    kernel = np.ones(k)/k
    return np.convolve(novelty, kernel, mode='same')


