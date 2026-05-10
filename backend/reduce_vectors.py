from gensim.models import KeyedVectors
import pickle

print("Loading full model (this will take a while)...")
try:
    model = KeyedVectors.load_word2vec_format(
        'cc.en.300.vec', 
        binary=False,
        encoding='utf-8',
        unicode_errors='ignore'
    )
except UnicodeDecodeError:
    # Try different encoding
    model = KeyedVectors.load_word2vec_format(
        'cc.en.300.vec', 
        binary=False,
        encoding='latin-2',
        unicode_errors='ignore'
    )

print(f"Loaded {len(model)} words")

# Filter to only words without underscores, numbers, etc.
clean_words = []
for word in model.index_to_key:
    # Keep only words that are:
    # - alphabetic (no numbers/punctuation)
    # - no underscores (removes phrases)
    # - is lowercase
    # - reasonable length (filters garbage)
    if word.isalpha() and '_' not in word and word.islower() and 5 <= len(word) <= 20:
        clean_words.append(word)

print(f"Filtered to {len(clean_words)} clean words")

# Keep only first 3k most common clean words (filtering out 100 most common ones though)
clean_words = clean_words[100:3100]

# Create reduced model dictionary
reduced_model = {word: model[word] for word in clean_words}

print(f"Saving reduced model with {len(reduced_model)} words...")
with open('reduced_vectors.pkl', 'wb') as f:
    pickle.dump(reduced_model, f)

print("Done! File saved as reduced_vectors.pkl")