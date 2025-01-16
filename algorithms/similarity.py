from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

def lcs_similarity(text1: List[str], text2: List[str]) -> float:
    """
    Calcule la similarité basée sur la plus longue sous-séquence commune.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    lcs_length = dp[m][n]
    max_length = max(m, n)
    return (lcs_length / max_length) * 100 if max_length > 0 else 0

def levenshtein_similarity(text1: List[str], text2: List[str]) -> float:
    """
    Calcule la similarité basée sur la distance de Levenshtein.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,    # deletion
                    dp[i][j-1] + 1,    # insertion
                    dp[i-1][j-1] + 1   # substitution
                )

    max_length = max(m, n)
    distance = dp[m][n]
    return (1 - (distance / max_length)) * 100 if max_length > 0 else 0

def cosine_similarity(text1: List[str], text2: List[str]) -> float:
    """
    Calcule la similarité cosinus entre deux textes.
    """
    # Création d'un vocabulaire unique
    vocab = list(set(text1 + text2))

    # Création des vecteurs
    vector1 = [text1.count(word) for word in vocab]
    vector2 = [text2.count(word) for word in vocab]

    # Calcul de la similarité cosinus
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    norm1 = sum(a * a for a in vector1) ** 0.5
    norm2 = sum(b * b for b in vector2) ** 0.5

    return (dot_product / (norm1 * norm2)) * 100 if norm1 * norm2 > 0 else 0
