import os
import logging as log

import rdflib
from rdflib import RDFS, RDF
from rdflib.term import URIRef, Literal
from rdflib.resource import Resource


class FoodOntology:

    def __init__(self, path):
        self.graph = rdflib.Graph()
        self.graph.parse(path, format='ttl')

        self.PERSON = self.get_class_resource("person")
        self.RECIPE = self.get_class_resource("recipe")
        self.CUISINE = self.get_class_resource("cuisine")
        self.FOOD = self.get_class_resource("food")

    def get_recipes(self, ingredients, cuisine, excluded_recipe, excluded_ingredients=[], excluded_cuisine=[]):

        query = """SELECT DISTINCT ?individual
WHERE {
  ?individual rdf:type owl:NamedIndividual .
  ?individual rdf:type :%s .""" % (self.RECIPE.qname(),)

        idx = 0
        ingredient_template = """
  ?ingredient%d rdf:type :%s .
  ?individual :hasIngredient ?ingredient%d ."""
        for ingredient in ingredients:
            query += ingredient_template % (idx, ingredient.qname(), idx)
            idx += 1

        excluded_ingredient_template = """
        MINUS { ?ingredient%d rdf:type :%s .
                ?individual :hasIngredient ?ingredient%d . }"""
        for excluded_ingredient in excluded_ingredients:
            query += excluded_ingredient_template % (idx, excluded_ingredient.qname(), idx)
            idx += 1

        cuisine_template = "\n  ?individual rdf:type :%s ."
        for cuisine_type in cuisine:
            query += cuisine_template % cuisine_type.qname()

        excluded_cuisine_template = "\n  MINUS { ?individual rdf:type :%s . }"
        for cuisine_type in excluded_cuisine:
            query += excluded_cuisine_template % cuisine_type.qname()

        query += "\n}"
        log.debug(query)
        result = self.graph.query(query)

        recipes = {}
        for row in result:
            recipe = Resource(self.graph, row[0])
            link = recipe.value(URIRef('http://www.semanticweb.org/ontologies/2019/0/project_giovanni#hasRelatedUrl'))
            recipes[recipe.label()] = {"recipe": recipe,
                                       "recipe_name": recipe.label(),
                                       "recipe_link": str(link)}

        for excluded in excluded_recipe:
            del recipes[excluded]

        return recipes

    def get_class_resource(self, label):
        """

        :param label:
        :return:
        """
        subject = self._get_class_by_label(label)

        resource = None
        if subject is not None:
            resource = Resource(self.graph, subject)

        return resource

    def is_subclass(self, resource, parent_resource):
        return parent_resource in resource.transitive_objects(RDFS.subClassOf)

    def _get_label(self, subject):
        if isinstance(subject, str):
            subject = URIRef(subject)
        return self.graph.label(subject)

    def _get_class_by_label(self, label):
        subjects = [s for s in self.graph.subjects(RDFS.label, Literal(label))]

        if len(subjects):
            if len(subjects) == 1:
                return subjects[0]
            else:
                raise Exception("Multiple subjects for the same label found!")
        else:
            return None

    def _print_statements(self):
        for stmt in self.graph:
            print(stmt)


def meat_test(onto):

    meat_resource = onto.get_class_resource("meat")
    chicken_resource = onto.get_class_resource("chicken")
    food_resource = onto.get_class_resource("food")

    print("Is chicken meat? ", onto.is_subclass(chicken_resource, meat_resource))
    print("Is all meat chicken? ", onto.is_subclass(meat_resource, chicken_resource))
    print("Is chicken food? ", onto.is_subclass(chicken_resource, food_resource))


def main():

    path = os.path.join(os.path.dirname(__file__), 'resources/project_giovanni.0.1.ttl')
    onto = FoodOntology(path)

    rice = onto.get_class_resource("rice")
    tomato = onto.get_class_resource("tomato")

    results = onto.get_recipes([rice, tomato], [], [])
    print(results)

    results = onto.get_recipes([rice], [], results)
    print(results)


if __name__ == "__main__":
    main()
