class RecommendationScorer:
    def __init__(self):
        pass

    def calculate_score(self, collab, content, popularity):
        # Normalize scores to avoid dominance
        return (
            0.5 * collab +
            0.3 * content +
            0.2 * popularity
        )

    def get_reason(self, collab, content, popularity):
        # Better reasoning logic (more varied)
        if collab > 1:
            return "recommended by similar users"
        elif content > 0:
            return "matches your interests"
        elif popularity > 2:
            return "trending item"
        else:
            return "general recommendation"

    def rank(self, user_id, candidates, context, limit=5):
        user_data = context["user_data"]
        item_data = context["item_data"]

        results = []

        user_items = set(user_data.get(user_id, []))

        for item in candidates:

            # -------------------------------
            # 1. Collaborative Score
            # -------------------------------
            collab = 0
            for other_user, items in user_data.items():
                if other_user == user_id:
                    continue

                similarity = len(user_items & items)
                if similarity > 0 and item in items:
                    collab += similarity

            # Normalize collab
            collab = collab / (len(user_data) or 1)

            # -------------------------------
            # 2. Content Score (FIXED)
            # -------------------------------
            user_categories = set(
                item_data.get(i) for i in user_items if i in item_data
            )

            item_category = item_data.get(item)

            content = 1 if item_category in user_categories else 0

            # -------------------------------
            # 3. Popularity Score
            # -------------------------------
            popularity = sum(item in items for items in user_data.values())
            popularity = popularity / (len(user_data) or 1)

            # -------------------------------
            # Final Score
            # -------------------------------
            score = self.calculate_score(collab, content, popularity)
            reason = self.get_reason(collab, content, popularity)

            results.append({
                "item": item,
                "score": round(score, 3),
                "reason": reason
            })

        # Sort
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:limit]