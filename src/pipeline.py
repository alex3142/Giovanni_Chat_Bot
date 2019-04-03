# -*- coding: utf-8 -*-
"""
@author: rcarlini
"""
import logging as log
log.basicConfig(level=log.INFO)

try:
    from .speech2text import Transcriber
except:
    log.warning("Transcriber not imported!")

from .ontology import FoodOntology
from .analysis import Analyzer
from .dialog_management import DialogManager, Utterance, State
from .generation import Generator, ResponseType
from .text2speech import Synthesizer


class Pipeline:

    def __init__(self, ontology_filepath):

        self.sessions = {'default': State()}

        try:
            self.transcriber = Transcriber()
        except:
            log.warning("Transcriber not loaded!")

        log.info("Loading ontology...")
        self.ontology = FoodOntology(ontology_filepath)
        log.info("Loading analyzer...")
        self.analyzer = Analyzer(self.ontology)
        log.info("Loading dialog manager...")
        self.dialog_manager = DialogManager(self.ontology)
        log.info("Loading generator...")
        self.generator = Generator()
        log.info("Loading synthesizer...")
        self.synthesizer = Synthesizer()

    def process_audio(self, audio_file, generate_audio=False, session_id='default'):
        text = self.transcriber.transcribe(audio_file)
        return self.process_text(text, generate_audio, session_id)

    def process_text(self, text, generate_audio=False, session_id='default'):
        try:
            if not text:
                response = self.generator.generate_utterance(Utterance(ResponseType.CLARIFY))

            else:
                concepts = self.analyzer.analyze(text)
                #print("concepts = ",concepts)
                utterance = self.dialog_manager.evaluate(self.sessions[session_id], concepts)
                response = self.generator.generate(utterance)

            if generate_audio:
                response = self.synthesizer.synthesize(response)

        except Exception as e:
            log.error(e)
            response = self.generator.generate_utterance(Utterance(ResponseType.ERROR))
            raise

        return response

    def new_session(self, bot_initiative=False, session_id='default', session_type='cmd'):
        self.sessions[session_id] = State()

        self.sessions[session_id].session_type = session_type
        self.sessions[session_id].has_initiative = bot_initiative
        if self.sessions[session_id].has_initiative:
            response = self.generator.generate_utterance(Utterance(ResponseType.GREETING_INITIATIVE))
        else:
            response = None

        return session_id, response

    def is_finished(self, session_id='default'):
        return self.sessions[session_id].finished

