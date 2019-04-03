# -*- coding: utf-8 -*-
import logging as log

from giovanni.generation import ResponseType


class State:
    """
    Stores the state of the conversation and the previous utterances.
    """

    def __init__(self):
        self.session_type = 'cmd'
        self.has_initiative = False
        self.recipe_asked = False
        self.finished = False

        self.ingredients = []
        self.excluded_ingredients = []
        self.cuisine = []
        self.excluded_cuisine = []

        self.previous_utterances = {}
        self.turns = []
        self.already_suggested = {}


class Utterance:
    """
    Describes the dialog action to be taken and the concepts to be used in that action.
    """

    def __init__(self, action, concepts=None):

        if concepts is None:
            concepts = {}

        self.action = action
        self.concepts = concepts

    def __repr__(self):
        return "%s#%s" % (self.action, str(self.concepts))


class DialogManager:
    """
    Evaluates the current state of the conversation, generating a conceptual utterance for the response.
    """

    def __init__(self, ontology):
        self.ontology = ontology

    def retrieve_recipe(self, state):

        recipes = self.ontology.get_recipes(state.ingredients, state.cuisine, state.already_suggested, state.excluded_ingredients, state.excluded_cuisine)

        for recipe in recipes.values():
            return recipe
        return None

    def suggest_recipe(self, state):
        recipe = self.retrieve_recipe(state)
        if recipe:
            state.already_suggested[recipe['recipe_name']] = recipe
            if state.session_type == 'html':
                utterances = {ResponseType.SUGGEST_RECIPE_LINK: Utterance(ResponseType.SUGGEST_RECIPE_LINK, recipe)}
            else:
                utterances = {ResponseType.SUGGEST_RECIPE: Utterance(ResponseType.SUGGEST_RECIPE, recipe)}
        else:
            # What do we do?!
            utterances = {ResponseType.APOLOGIZE_NO_RECIPE: Utterance(ResponseType.APOLOGIZE_NO_RECIPE)}

        return utterances

    def handle_wants_recipe(self, state):

        utterances = {}
        if len(state.ingredients) == 0 and \
                ResponseType.REQUEST_INGREDIENTS not in state.previous_utterances:
            utterances[ResponseType.REQUEST_INGREDIENTS] = Utterance(ResponseType.REQUEST_INGREDIENTS)
            """
        elif len(self.state.ingredients) < 3:
            # Try requesting more ingredients?
            pass
            """
        elif len(state.cuisine) == 0 and \
                ResponseType.REQUEST_CUISINE not in state.previous_utterances:
            utterances[ResponseType.REQUEST_CUISINE] = Utterance(ResponseType.REQUEST_CUISINE)

        elif state.turns:
            last_turn = state.turns[-1]

            if ResponseType.SUGGEST_LINK in last_turn or \
                    ResponseType.SUGGEST_RECIPE_LINK in last_turn:
                utterances = {ResponseType.FAREWELL: Utterance(ResponseType.FAREWELL)}

            elif ResponseType.GREETING_INITIATIVE in last_turn or \
                    ResponseType.SUGGEST_RECIPE in last_turn:

                suggested_recipe = last_turn[ResponseType.SUGGEST_RECIPE].concepts
                utterances[ResponseType.SUGGEST_LINK] = Utterance(ResponseType.SUGGEST_LINK, suggested_recipe)

            else:
                utterances = self.suggest_recipe(state)
        return utterances

    def handle_disagreement(self, state):

        last_turn = state.turns[-1]
        if ResponseType.GREETING_INITIATIVE in last_turn:
            utterances = {ResponseType.FAREWELL: Utterance(ResponseType.FAREWELL)}

        elif ResponseType.SUGGEST_RECIPE in last_turn or \
                ResponseType.SUGGEST_RECIPE_LINK in last_turn:
            utterances = self.suggest_recipe(state)

        else:
            utterances = {}

        return utterances

    def handle_triples(self, state: State, triples):

        idx = 0
        while idx < len(triples):
            triple = triples[idx]

            try:
                print(triple[0].label(), triple[1], triple[2].label())
            except IndexError:
                print(triple[0].label(), triple[1])

            if triple[0] == self.ontology.PERSON:

                if triple[1] in ('has', 'HasRelationship'):
                    if self.ontology.is_subclass(triple[2], self.ontology.FOOD):
                        state.ingredients.append(triple[2])
                        triples.pop(idx)
                        idx -= 1

                if triple[1] in ('NotHasRelationship',):
                    if self.ontology.is_subclass(triple[2], self.ontology.FOOD):
                        state.excluded_ingredients.append(triple[2])
                        triples.pop(idx)
                        idx -= 1

                elif triple[1] in ('wants', 'WantsRelationship'):
                    if self.ontology.is_subclass(triple[2], self.ontology.CUISINE):
                        state.cuisine.append(triple[2])
                        triples.pop(idx)
                        idx -= 1

                elif triple[1] in ('NotWantsRelationship',):
                    if self.ontology.is_subclass(triple[2], self.ontology.CUISINE):
                        state.excluded_cuisine.append(triple[2])
                        triples.pop(idx)
                        idx -= 1
            idx += 1

        utterances = {}
        for triple in triples:
            if triple[0] == self.ontology.PERSON:
                if triple[1] in ('greeting',):
                    utterances[ResponseType.GREETING] = Utterance(ResponseType.GREETING)

                elif triple[1] in ('swearing',):
                    utterances[ResponseType.SWEAR_ANSWER] = Utterance(ResponseType.SWEAR_ANSWER)

                elif triple[1] in ('farewell',):
                    utterances = {ResponseType.FAREWELL: Utterance(ResponseType.FAREWELL)}
                    state.finished = True
                    break

                elif triple[1] in ('wants', 'WantsRelationship'):
                    if triple[2] == self.ontology.RECIPE:
                        state.recipe_asked = True

                elif triple[1] == 'agreement':
                    if state.turns and ResponseType.GREETING_INITIATIVE in state.turns[-1]:
                        state.recipe_asked = True

                elif triple[1] == 'NOTagreement':
                    utterances = self.handle_disagreement(state)

                elif triple[1] == 'indifference':
                    # Ignored, is handled in handle wants recipe
                    pass

        if state.recipe_asked and \
                ResponseType.SUGGEST_RECIPE not in utterances and \
                ResponseType.SUGGEST_RECIPE_LINK not in utterances and \
                ResponseType.FAREWELL not in utterances:
            utterances.update(self.handle_wants_recipe(state))

        if not utterances:
            utterances[ResponseType.CLARIFY] = Utterance(ResponseType.CLARIFY)

        return utterances

    def evaluate(self, state, triples):
        """
        Given a list of nouns, extracts the ingredients and cuisine types from it and adds them to the state. If there
        is something missing, asks for it, otherwise, suggests a recipe given the current state.

        :param state:
        :param triples:
        :return: A conceptual utterance for the response.
        """

        if triples:
            utterances = self.handle_triples(state, triples)
        else:
            utterances = {ResponseType.CLARIFY: Utterance(ResponseType.CLARIFY)}

        state.turns.append(utterances)
        state.previous_utterances.update(utterances)

        log.debug(utterances)
        return utterances
