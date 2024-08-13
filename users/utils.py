import math
from collections import Counter

def cosine_similarity(text1, text2):
    # Tokenize the texts
    words1 = text1.split()
    words2 = text2.split()

    # Count the word frequencies
    freq1 = Counter(words1)
    freq2 = Counter(words2)

    # Find the intersection of the words
    intersection = set(freq1.keys()) & set(freq2.keys())

    # Calculate the dot product
    dot_product = sum([freq1[word] * freq2[word] for word in intersection])

    # Calculate the magnitudes
    magnitude1 = math.sqrt(sum([freq1[word]**2 for word in freq1]))
    magnitude2 = math.sqrt(sum([freq2[word]**2 for word in freq2]))

    # Avoid division by zero
    if not magnitude1 or not magnitude2:
        return 0.0

    # Calculate cosine similarity
    return dot_product / (magnitude1 * magnitude2)
