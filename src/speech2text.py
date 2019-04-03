import speech_recognition as speech_rec

class Transcriber:

    def __init__(self):
        self.recognizer = speech_rec.Recognizer()

    def transcribe(self, audio_file):
        """
        Transcribes the input audio file to text.

        :param audio_file: path to the audio file with the speech to decode
        :return: text string with the decoded speech
        """

        af = speech_rec.AudioFile(audio_file)
        with af as source:
            audio = self.recognizer.record(source)
        text = self.recognizer.recognize_google(audio_data=audio,show_all=False) # show_all = True will display many guesses for the sentence

        return text