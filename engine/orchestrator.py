from engine.candidate_gen import CandidateGenerator
from engine.scorer import RecommendationScorer


class RecommendationOrchestrator:
    def __init__(self, user_repo, content_repo, interaction_repo):
        self.user_repo = user_repo
        self.content_repo = content_repo
        self.interaction_repo = interaction_repo

        self.candidate_gen = CandidateGenerator(
            user_repo, content_repo, interaction_repo
        )
        self.scorer = RecommendationScorer()
        self.cache = {}

    def get_recommendations(self, user_id, limit=5):

        #  Cache check
        if user_id in self.cache:
            return self.cache[user_id]

        # Load data
        user_data = self.candidate_gen._load_user_data()
        item_data = self.candidate_gen._load_item_data()

        # Generate candidates
        candidates = self.candidate_gen.hybrid_candidates(user_id)

        #  Structured context for ML scoring
        context = {
            "user_data": user_data,
            "item_data": item_data
        }

        # Rank candidates
        ranked = self.scorer.rank(
            user_id,
            candidates,
            context,
            limit
        )

        #  Cache result
        self.cache[user_id] = ranked

        return ranked

    #  OPTIONAL: clear cache when feedback happens
    def clear_cache(self, user_id=None):
        if user_id:
            self.cache.pop(user_id, None)
        else:
            self.cache.clear()