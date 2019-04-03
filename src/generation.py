# -*- coding: utf-8 -*-
import random
from enum import Enum


class ResponseType(Enum):
    REQUEST_INGREDIENTS = 1
    REQUEST_CUISINE = 2
    SUGGEST_RECIPE = 3
    SUGGEST_LINK = 4
    SUGGEST_RECIPE_LINK = 5
    APOLOGIZE_NO_RECIPE = 6
    GREETING = 7
    GREETING_INITIATIVE = 8
    FAREWELL = 9
    CLARIFY = 10
    SWEAR_ANSWER = 11
    ERROR = 12


response_templates = {
    ResponseType.REQUEST_INGREDIENTS: [
        "Sure, what ingredients do you have?",
        "Ok, what ingredients do you have available?",
        "What ingredients do you have to hand?",
        "What ingredients do you have in the kitchen?"
    ],

    ResponseType.REQUEST_CUISINE: [
        #"Do you like a specific cuisine type?",
        "What type of cuisine do you like?",
        "Tell me your favourite cuisine.",
        "What cuisines are you interested in?",
        "What cuisine do you have in mind?"
        #"Do you have any preference on cuisine?",
        #"Sure, do you have a cuisine in mind?",
        #"Any particular cuisine?"
    ],

    ResponseType.SUGGEST_RECIPE: [
        "How about {recipe_name}?",
        "What about {recipe_name}?",
        "Does {recipe_name} sound good?",
        "I recommend {recipe_name}."
    ],

    ResponseType.SUGGEST_RECIPE_LINK: [
        "How about <a href='{recipe_link}'>{recipe_name}</a>?",
        "What about <a href='{recipe_link}'>{recipe_name}</a>?",
        "Does <a href='{recipe_link}'>{recipe_name}</a> sound good?",
        "I recommend <a href='{recipe_link}'>{recipe_name}</a>."
    ],

    ResponseType.SUGGEST_LINK: [
        "Here is the link: <a href='{recipe_link}'>{recipe_name}</a>.",
        "Enjoy your recipe {recipe_link}.",
        "You can find the recipe here {recipe_link}.",
        "Here's your recipe {recipe_link}."
    ],

    ResponseType.APOLOGIZE_NO_RECIPE: [
        "I'm sorry, I don't know any suitable recipe."
    ],

    ResponseType.GREETING: [
        "Hi.",
        "Hello.",
        "Hi there.",
        "Hey!",
        "How's it going?"
    ],

    ResponseType.GREETING_INITIATIVE: [
        "Hi, it's me, Giovanni! Are you looking for a recipe?"
    ],

    ResponseType.FAREWELL: [
        "Hasta la vista, baby.",
        "Have a nice day.",
        "Good bye.",
        "Farewell.",
        "Bye.",
        "Adios.",
        "Hopefully speak to you soon!"
    ],

    ResponseType.CLARIFY: [
        "Can you repeat it?",
        "Can you say that again?",
        "I didn't understand that, can you repeat it please?",
        "I'm not sure I understood what you meant, can you try again please?",
        "I didn't quite understand, would you mind saying that again?",
        "I didn't get that can you repeat what you just said?",
        "Would you mind just clarifying that?"
    ],

    ResponseType.SWEAR_ANSWER: [
        "There is no need for that language.",
        "Alright bambino calm down.",
        "I'm too young to hear such language.",
        "Ok ok, chill out.",
        "Ugh, I should have applied for the job as Alexa."
    ],

    ResponseType.ERROR: [
        "Dave, my mind is going. I can feel it.",
        "I'm sorry clearly there has been a horrendous error.",
        "Well, isn't this embarrassing, an error has occured."
    ]
}


class Response:

    def __init__(self):
        self.templates = []
        self.parts = []

    def add(self, template, message):
        self.templates.append(template)
        self.parts.append(message)

    def __str__(self):
        return " ".join(self.parts)


class Generator:

    def generate_utterance(self, utterance):

        templates = response_templates[utterance.action]
        chosen_response = random.choice(templates)
        return chosen_response, chosen_response.format(**utterance.concepts)

    def generate(self, utterances):

        response = Response()

        if ResponseType.GREETING in utterances:
            template, message = self.generate_utterance(utterances[ResponseType.GREETING])
            response.add(template, message)
            del utterances[ResponseType.GREETING]

        for utterance in utterances.values():
            template, message = self.generate_utterance(utterance)
            response.add(template, message)

        return response
