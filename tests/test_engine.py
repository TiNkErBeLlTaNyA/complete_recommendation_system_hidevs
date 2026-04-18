from data.database import SessionLocal
from data.repositories import UserRepository, ContentRepository, InteractionRepository
from engine.orchestrator import RecommendationOrchestrator


def test_recommendations_return():
    db = SessionLocal()

    orchestrator = RecommendationOrchestrator(
        UserRepository(db),
        ContentRepository(db),
        InteractionRepository(db)
    )

    recs = orchestrator.get_recommendations(1)

    assert recs is not None
    assert isinstance(recs, list)
    assert len(recs) > 0

    # Check structure of recommendation
    item = recs[0]
    assert "item" in item
    assert "score" in item
    assert "reason" in item


def test_recommendations_sorted():
    db = SessionLocal()

    orchestrator = RecommendationOrchestrator(
        UserRepository(db),
        ContentRepository(db),
        InteractionRepository(db)
    )

    recs = orchestrator.get_recommendations(1)

    scores = [r["score"] for r in recs]

    # Ensure sorted in descending order
    assert scores == sorted(scores, reverse=True)


def test_cold_start():
    db = SessionLocal()

    orchestrator = RecommendationOrchestrator(
        UserRepository(db),
        ContentRepository(db),
        InteractionRepository(db)
    )

    recs = orchestrator.get_recommendations(999)  # new user

    assert len(recs) > 0