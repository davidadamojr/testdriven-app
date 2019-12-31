import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Score


class TestScoresService(BaseTestCase):
    """Tests for the Scores Service"""

    def test_all_scores(self):
        """Ensure get all scores behaves correctly"""
        self._add_score(1, 1, True)
        self._add_score(1, 2, False)

        with self.client:
            response = self.client.get("/scores")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["scores"]), 2)
            self.assertEqual(data["data"]["scores"][0]["user_id"], 1)
            self.assertEqual(data["data"]["scores"][0]["exercise_id"], 1)
            self.assertTrue(data["data"]["scores"][0]["correct"])
            self.assertEqual(data["data"]["scores"][1]["user_id"], 1)
            self.assertEqual(data["data"]["scores"][1]["exercise_id"], 2)
            self.assertFalse(data["data"]["scores"][1]["correct"])

    def test_all_scores_by_user(self):
        """Ensure get all scores by user behaves correctly"""
        self._add_score(1, 1, True)
        self._add_score(1, 2, False)
        self._add_score(2, 1, True)

        with self.client:
            response = self.client.get("/scores/1")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["scores"]), 2)
            self.assertEqual(data["data"]["scores"][0]["user_id"], 1)
            self.assertEqual(data["data"]["scores"][0]["exercise_id"], 1)
            self.assertTrue(data["data"]["scores"][0]["correct"])
            self.assertEqual(data["data"]["scores"][1]["user_id"], 1)
            self.assertEqual(data["data"]["scores"][1]["exercise_id"], 2)
            self.assertFalse(data["data"]["scores"][1]["correct"])

    def test_single_score_by_user(self):
        """Ensure get single score by user behaves correctly"""
        self._add_score(1, 1, True)
        self._add_score(1, 2, False)

        with self.client:
            response = self.client.get("/scores/user/1")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["data"]["score"]["user_id"], 1)
            self.assertEqual(data["data"]["score"]["exercise_id"], 1)
            self.assertTrue(data["data"]["score"]["correct"])

    def test_add_score(self):
        """Ensure adding a score behaves correctly"""
        with self.client:
            response = self.client.post(
                "/scores",
                data=json.dumps(
                    {"user_id": 1, "exercise_id": 1, "correct": True}
                ),
                content_type="application/json",
                headers=({"Authorization": "Bearer test"}),
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("New score was added!", data["message"])
            self.assertIn("Success", data["status"])

    def test_update_score_by_exercise_id(self):
        """Ensure updating a score behaves correctly"""
        self._add_score(1, 1, True)

        with self.client:
            response = self.client.put(
                "/scores/1",
                data=json.dumps({"correct": False}),
                content_type="application/json",
                headers=({"Authorization": "Bearer test"}),
            )
            data = json.loads(response.data.decode())
            self.assertFalse(data["data"]["correct"])
            self.assertEqual(response.status_code, 200)
            self.assertIn("Score was updated!", data["message"])
            self.assertIn("Success", data["status"])

    @staticmethod
    def _add_score(user_id, exercise_id, correct):
        db.session.add(
            Score(user_id=user_id, exercise_id=exercise_id, correct=correct)
        )
        db.session.commit()
