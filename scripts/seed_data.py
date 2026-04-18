from data.database import SessionLocal, engine, Base
from data.models import User, Content, Interaction
import random

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear old data (important for re-runs)
db.query(Interaction).delete()
db.query(User).delete()
db.query(Content).delete()
db.commit()

# Diverse interests
interests_list = ["AI", "ML", "Data Science", "Web Dev"]

# Users
for i in range(1, 11):
    db.add(User(
        id=i,
        name=f"User{i}",
        interests=random.choice(interests_list)
    ))

# Diverse categories
categories = ["AI", "ML", "Data Science", "Web Dev"]

# Content
for i in range(1, 21):
    db.add(Content(
        id=i,
        title=f"Course{i}",
        category=random.choice(categories),
        difficulty=random.choice(["easy", "medium", "hard"]),
        popularity=random.randint(1, 20)
    ))

# Interactions (more realistic)
for i in range(1, 11):
    interacted_items = random.sample(range(1, 21), 5)

    for item in interacted_items:
        db.add(Interaction(
            user_id=i,
            content_id=item,
            type=random.choice(["view", "click"]),
            rating=random.randint(1, 5)
        ))

db.commit()
db.close()

print(" Database seeded successfully")