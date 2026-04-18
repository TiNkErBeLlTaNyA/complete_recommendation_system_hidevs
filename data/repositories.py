from .models import User, Content, Interaction


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_interactions(self, user_id):
        return self.db.query(Interaction).filter_by(user_id=user_id).all()

    def all(self):
        return self.db.query(User).all()


class ContentRepository:
    def __init__(self, db):
        self.db = db

    def all(self):
        return self.db.query(Content).all()

    def get(self, content_id):
        return self.db.query(Content).filter(Content.id == content_id).first()

    # NEW: useful for scoring
    def get_popular(self, limit=5):
        return self.db.query(Content).order_by(Content.popularity.desc()).limit(limit).all()


class InteractionRepository:
    def __init__(self, db):
        self.db = db

    def add(self, interaction):
        try:
            self.db.add(interaction)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def get_all(self):
        return self.db.query(Interaction).all()

    #  NEW: interactions for specific content
    def get_by_content(self, content_id):
        return self.db.query(Interaction).filter_by(content_id=content_id).all()

    #  NEW: interactions for specific user
    def get_by_user(self, user_id):
        return self.db.query(Interaction).filter_by(user_id=user_id).all()