import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:

    def user_similarity(self, user_item_matrix):
        """
        Compute cosine similarity between users
        """
        if user_item_matrix is None or len(user_item_matrix) == 0:
            return np.array([])

        return cosine_similarity(user_item_matrix)

    def item_similarity(self, item_matrix):
        """
        Compute similarity between items
        """
        if item_matrix is None or len(item_matrix) == 0:
            return np.array([])

        return cosine_similarity(item_matrix)