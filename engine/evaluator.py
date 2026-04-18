import math


class RecommendationEvaluator:

    # Convert objects → item IDs safely
    def _extract_ids(self, recs):
        if isinstance(recs[0], dict):
            return [r["item"] for r in recs]
        return recs

    def precision_at_k(self, recs, relevant, k):
        rec_ids = self._extract_ids(recs)
        return len(set(rec_ids[:k]) & set(relevant)) / k if k else 0

    def recall_at_k(self, recs, relevant, k):
        rec_ids = self._extract_ids(recs)
        return len(set(rec_ids[:k]) & set(relevant)) / len(relevant) if relevant else 0

    def ndcg_at_k(self, recs, relevant, k):
        rec_ids = self._extract_ids(recs)

        dcg = sum(
            1 / math.log2(i + 2)
            for i, item in enumerate(rec_ids[:k])
            if item in relevant
        )

        idcg = sum(
            1 / math.log2(i + 2)
            for i in range(min(len(relevant), k))
        )

        return dcg / idcg if idcg else 0

    def evaluate(self, recs, relevant, k=5):
        return {
            "precision@5": self.precision_at_k(recs, relevant, k),
            "recall@5": self.recall_at_k(recs, relevant, k),
            "ndcg@5": self.ndcg_at_k(recs, relevant, k)
        }