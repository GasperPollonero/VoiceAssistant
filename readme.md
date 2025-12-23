# Project Duccio
### a custum voice assistant using only open source software

This is an educational project aimed at programming a full functioning AI voice assistant.
The project consists in putting several pieces of softwares all together. It is composed both by external open source models and self-trained models and is mainly composed by three components:
- Speech To Text (STT)
- Natural Language Processing (NLP)
- Text To Speech (TTS)

### STT
The STT is the first part, which converts the vocal command spoke by the user to a text for elaboration. The STT used in this project is   [whisper](https://github.com/openai/whisper) from OpenAI that you need to download and compile. It should be easy to implement another STT of your choice by changing some lines in [STT.py](./STT.py).

### NLP

The NLP is the piece in charge of elaborating the user's requests and producing an output. 
You can use [intent_train.py](./intent_train.py) to train your simple model on a custom database using LogisticRegression and saving the results under /models/intent/. Then, [intent_ml.py](./intent_ml.py) uses the model to produce an output starting from an input text. [NLP.py](./NLP.py) gives the input to intent_ml.py, reads the output label and perform the action based on it.

### TTS
The TTS is the last piece, the one that accompanies the output with a synthesized voice.
The TTS used in this project is [piper](https://github.com/rhasspy/piper) made by Rhasspy.