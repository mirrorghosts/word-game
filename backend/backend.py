from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import pickle
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
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

# No more KeyedVectors
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

def get_similar_words(word: str, target: str, topn: int = 5):
    if word not in model_dict:
        return []
    
    vec1 = model_dict[word]
    vec2 = model_dict[target]

    current_to_target = cosine_similarity(vec1, vec2)

    similarities = []

    print(f"Current word '{word}' similarity to target '{target}': {current_to_target}")
    
    for other_word, other_vec in model_dict.items():
        if other_word == word:
            continue

        if other_word == target and current_to_target < 0.3:
            continue

        sim1 = cosine_similarity(vec1, other_vec)
        sim2 = cosine_similarity(other_vec, vec2)

        if sim2 > current_to_target:
            progress = sim2 - current_to_target
            score = sim1 + progress
        else:
            score = sim1 * 0.5

        similarities.append((other_word, score))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    result = [w for w, score in similarities[:topn]]

    random.shuffle(result)

    print(f"RETURNING TO FRONTEND: {result}")
    return result

@app.get("/get_next_words/{word}/{target}")
def get_next_words(word: str, target: str):
    return {"next_words": get_similar_words(word, target)}

@app.get("/get_random_words")
def get_random_words():
    start_word = random.choice(vocab)
    target_word = random.choice(vocab)
    
    while target_word == start_word:
        target_word = random.choice(vocab)

    return {"start_word": start_word, "target_word": target_word}