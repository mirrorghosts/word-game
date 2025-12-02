from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import pickle
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load reduced model
print("Loading reduced model...")
with open('reduced_vectors.pkl', 'rb') as f:
    model_dict = pickle.load(f)

vocab = list(model_dict.keys())
print(f"Loaded {len(vocab)} words")

# Since we're not using KeyedVectors anymore, we calculate similarity manually
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

def get_similar_words(word: str, topn: int = 10):
    if word not in model_dict:
        return []
    
    target_vec = model_dict[word]
    similarities = []
    
    for other_word, other_vec in model_dict.items():
        if other_word != word:
            sim = cosine_similarity(target_vec, other_vec)
            similarities.append((other_word, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [w for w, score in similarities[:topn]]

@app.get("/get_next_words/{word}")
def get_next_words(word: str):
    return {"next_words": get_similar_words(word)}

@app.get("/get_random_words")
def get_random_words():
    start_word = random.choice(vocab)
    target_word = random.choice(vocab)
    
    while target_word == start_word:
        target_word = random.choice(vocab)

    return {"start_word": start_word, "target_word": target_word}