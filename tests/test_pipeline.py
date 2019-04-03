from unittest import TestCase

from giovanni.pipeline import Pipeline
from giovanni.generation import response_templates, ResponseType


class TestPipeline(TestCase):

    def setUp(self):
        self.pipeline = Pipeline('../resources/project_giovanni.0.1.ttl')

    def test_simple(self):
        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Rice")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("Italian")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE])
        self.assertIn("risotto", response.parts[0])

    def test_triple_hi(self):
        response = self.pipeline.process_text("Hi!")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

        response = self.pipeline.process_text("Hi!")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

        response = self.pipeline.process_text("Hi!")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

    def test_cuisine_no(self):
        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Chicken")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("No")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE])

    def test_recipe_no(self):
        response = self.pipeline.process_text("Hi, can you suggest a recipe?")

        self.assertEqual(len(response.templates), 2)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])
        self.assertIn(response.templates[1], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Rice and garlic.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("Any.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE])

        response = self.pipeline.process_text("No.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE])

    def test_cuisine_g(self):
        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Chicken")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("g")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.CLARIFY])

    def test_cuisine_italian(self):
        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Chicken")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("yeah, italian")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.APOLOGIZE_NO_RECIPE])

    def test_hi_fuck_you(self):
        response = self.pipeline.process_text("Hi!")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

        response = self.pipeline.process_text("fuck you")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SWEAR_ANSWER])

        response = self.pipeline.process_text("fuck you")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SWEAR_ANSWER])

    def test_hi_chicken(self):
        response = self.pipeline.process_text("Hi, i have chicken, can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("I like italian cuisine.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.APOLOGIZE_NO_RECIPE])

    def test_hi_have_chicken(self):
        response = self.pipeline.process_text("Hi.")
        """
        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])
        """
        response = self.pipeline.process_text("I have chicken.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

    def test_sure(self):
        response = self.pipeline.process_text("Cna you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Rice")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("Italian")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE])
        self.assertIn("risotto", response.parts[0])

        response = self.pipeline.process_text("Sure")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_LINK])

    def test_yes(self):
        response = self.pipeline.process_text("Cna you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Rice")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("Italian")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE])
        self.assertIn("risotto", response.parts[0])

        response = self.pipeline.process_text("Yes")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_LINK])
