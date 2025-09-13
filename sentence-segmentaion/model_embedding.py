from sentence_transformers import SentenceTransformer

def embed_sentences(sents, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
    # 2) Embeddings
    model = SentenceTransformer(model_name)
    # model = SentenceTransformer('VietAI/ViT5-base')
    E = model.encode(sents, normalize_embeddings=True)
    return E