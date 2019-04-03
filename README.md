## Giovanni recipe bot repository BETA
-------------------------------------------------------------------------------------

Copyright 2019 Alex G

Permission is hereby granted, free of charge, 
to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation
 the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the 
 Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 
 -------------------------------------------------------------------------------------

This is a basic recipe chat bot with both a voice and text interface.
The user can provide (currently only a limited set of) ingredients 
and a cuisine type (e.g. French cuisine) and the chat bot will suggest
a recipe containing the ingredients. Currently the ontology is fairly
sparse as this is just a proof of concept. 

This peice of work was built by a team of 3 for a university project, 
it is currently on git hub as an example of what has been produced by the team.

It should work using the command line interface (see below) however can also be 
configured to run in a web browser. In future (after I graduate) the code will be
fully configured, due to other course commitments there is not sufficent time
to package up this tool.

__work in progress__

Setup:

- Install python 3.x
- Install pip
- Run `pip install -r requirements` in order to install the current requirements.
- Download spacy models by running `python -m spacy download en`


There are two interfaces, currently:

- Web interface: The server.py program currently starts a flask server at localhost:9999 that allows the user to record and send audios to the server. (Currently doesn't work because the web interface encodes the audio as ogg and the speech recognition does not work with that format.)

- Command-line interface: The pipeline.py module allows to be run from the terminal. Is prepared to process .wav and .txt.

In order to test the interfaces, there are some .wav files in the Download section of the bitbucket repository ([pot_tea.wav](https://bitbucket.org/nlp_miis_upf/chat_bot_repo/downloads/pot_tea.wav), [chicken_leg.wav](https://bitbucket.org/nlp_miis_upf/chat_bot_repo/downloads/pot_tea.wav), [rice_bowls.wav.wav](https://bitbucket.org/nlp_miis_upf/chat_bot_repo/downloads/rice_bowls.wav)).

Also you'll find there our initial presentation of the project: [UPtoD8 chat bot.pptx](https://bitbucket.org/nlp_miis_upf/chat_bot_repo/downloads/UPtoD8%20chat%20bot.pptx).
