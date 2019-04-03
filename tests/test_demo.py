from unittest import TestCase

from giovanni.pipeline import Pipeline
from giovanni.generation import response_templates, ResponseType


class TestPipeline(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPipeline, self).__init__(*args, **kwargs)
        self.pipeline = Pipeline('../resources/project_giovanni.0.2.ttl', )

    def setUp(self):
        self.pipeline.new_session(session_type='html')

    def test_demo1(self):
        response = self.pipeline.process_text("Hi.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Rice")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("Italian")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE_LINK])
        self.assertIn("risotto", response.parts[0])

        response = self.pipeline.process_text("Sure")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.FAREWELL])

    def test_demo2(self):
        response = self.pipeline.process_text("Hi.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])

        response = self.pipeline.process_text("Can you suggest a recipe?")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_INGREDIENTS])

        response = self.pipeline.process_text("Rice, eggs, garlic, but not tomatoes or chicken.")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("chinese or french but not italian or african")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE_LINK])
        self.assertIn("Fried rice with prawns and chorizo", response.parts[0])

        response = self.pipeline.process_text("Sure")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.FAREWELL])

    def test_demo3(self):
        response = self.pipeline.process_text("Hi, can you suggest something with tomatoes and onion but not chicken.")

        self.assertEqual(len(response.templates), 2)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])
        self.assertIn(response.templates[1], response_templates[ResponseType.REQUEST_CUISINE])

        response = self.pipeline.process_text("chinese or french but not italian or african")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE_LINK])
        self.assertIn("Fried rice with prawns and chorizo", response.parts[0])

        response = self.pipeline.process_text("Sure")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.FAREWELL])

    def test_demo4(self):
        response = self.pipeline.process_text("Hi, can you suggest something spanish with rice and onion but not beef or peas.")

        self.assertEqual(len(response.templates), 2)
        self.assertIn(response.templates[0], response_templates[ResponseType.GREETING])
        self.assertIn(response.templates[1], response_templates[ResponseType.SUGGEST_RECIPE_LINK])
        self.assertIn("chicken paella", response.parts[0])

        response = self.pipeline.process_text("No")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.SUGGEST_RECIPE_LINK])
        self.assertIn("seafood paella", response.parts[0])

        response = self.pipeline.process_text("ok, thanks")

        self.assertEqual(len(response.templates), 1)
        self.assertIn(response.templates[0], response_templates[ResponseType.FAREWELL])
