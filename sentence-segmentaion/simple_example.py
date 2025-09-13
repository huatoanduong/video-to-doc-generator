from model_embedding import embed_sentences
from segmentation import calculate_novelty_score, segment_text
from sentence_processing import sentences_from_text
MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
text = "Hello, how are you? I am fine, thank you."

def segment_sentance(text):
    text = text.lower()
    sentences = sentences_from_text(text)
    embedded_sentences = embed_sentences(sentences, model_name=MODEL_NAME)
    novelty_score = calculate_novelty_score(embedded_sentences)
    segments = segment_text(sentences, novelty_score)
    return segments

if __name__ == "__main__":
    with open('M03W02 - K Nearest Neighbor (KNN).txt', 'r') as file:
        text = file.read()
    segments = segment_sentance(text)
    print(segments)


