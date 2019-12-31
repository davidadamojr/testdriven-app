from project import db


class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer)
    correct = db.Column(db.Boolean)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "exercise_id": self.exercise_id,
            "correct": self.correct,
        }
