from collections import defaultdict


class CandidateGenerator:

    def __init__(self, user_repo, content_repo, interaction_repo):
        self.user_repo = user_repo
        self.content_repo = content_repo
        self.interaction_repo = interaction_repo

    # Load user → items mapping
    def _load_user_data(self):
        user_data = defaultdict(set)
        for i in self.interaction_repo.get_all():
            user_data[i.user_id].add(i.content_id)
        return user_data

    # Load item → category
    def _load_item_data(self):
        item_data = {}
        for c in self.content_repo.all():
            item_data[c.id] = c.category
        return item_data

    # Collaborative filtering (similar users)
    def collaborative_candidates(self, user_id, user_data):
        target_items = user_data.get(user_id, set())
        scores = defaultdict(int)

        for other_user, items in user_data.items():
            if other_user == user_id:
                continue

            # similarity = intersection
            similarity = len(target_items & items)

            if similarity > 0:
                for item in items:
                    if item not in target_items:
                        scores[item] += similarity

        return list(scores.keys())

    # Content-based filtering
    def content_candidates(self, user_id, user_data, item_data):
        target_items = user_data.get(user_id, set())
        target_categories = set()

        for item in target_items:
            if item in item_data:
                target_categories.add(item_data[item])

        candidates = []
        for item, category in item_data.items():
            if category in target_categories and item not in target_items:
                candidates.append(item)

        return candidates

    # Popularity fallback
    def popularity_candidates(self, user_data):
        count = defaultdict(int)
        for items in user_data.values():
            for item in items:
                count[item] += 1

        return sorted(count, key=count.get, reverse=True)

    # Hybrid candidate generation
    def hybrid_candidates(self, user_id):
        user_data = self._load_user_data()
        item_data = self._load_item_data()

        # Cold start
        if user_id not in user_data:
            return self.popularity_candidates(user_data)

        collab = self.collaborative_candidates(user_id, user_data)
        content = self.content_candidates(user_id, user_data, item_data)
        popular = self.popularity_candidates(user_data)

        # Combine (remove duplicates, keep order)
        combined = collab + content + popular

        seen = set()
        unique_candidates = []

        for item in combined:
            if item not in seen:
                seen.add(item)
                unique_candidates.append(item)

        return unique_candidates