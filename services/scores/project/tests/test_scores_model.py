from project.tests.base import BaseTestCase
from project import db
from project.api.models import Score


class TestScoresModel(BaseTestCase):
    def test_add_score(self):
        # Arrange
        score = Score(user_id=1, exercise_id=1, correct=True)

        # Act
        db.session.add(score)
        db.session.commit()

        # Assert
        self.assertIsNotNone(score.id)
