import re, numpy as np, ruptures as rpt
from sentence_processing import calculate_novalty, normalize_novelty, moving_average

def calculate_novelty_score(embedded_sentences, w=15):
    novelty = calculate_novalty(embedded_sentences, w)
    return normalize_novelty(novelty)

def segment_text(sents, novelty_s, pen = 10, min_len = 6, k = 50):
    # 5) Change points với PELT trên 1D
    smoothed_novelty = moving_average(novelty_s, k= k)
    algo = rpt.Pelt(model="rbf").fit(novelty_s.reshape(-1, 1))
    bkps = algo.predict(pen= pen)  # thử 10–20; tăng giảm để được số đoạn mong muốn
    # 6) Áp min segment length & tạo đoạn
    filtered = []
    prev = 0
    for b in bkps:
        if b - prev < min_len:  # quá ngắn -> bỏ ranh giới này
            continue
        filtered.append(b)
        prev = b
    bkps = filtered

    segments = []
    start = 0
    for b in bkps:
        segments.append((start, b))
        start = b
    if start < len(sents):
        segments.append((start, len(sents)))
    return segments