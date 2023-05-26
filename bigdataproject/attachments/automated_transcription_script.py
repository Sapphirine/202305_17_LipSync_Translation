# -*- coding: utf-8 -*-
"""TRANSCRIPTION_SCRIPT_VK.ipynb

"""
# Download the necessary Package
from google.cloud import speech
from google.cloud import translate
from google.cloud import texttospeech
import os
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '<Keys location>'
# globals
PROJECT_ID = '<>'
PARENT = f"projects/{PROJECT_ID}"

"""# Send request to google cloud"""
# Step 1
def extract_text_from_audio(audio_file):
    # the path of your audio file
    # Read the audio file
    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    # Define Configuration File for loading language code etc.
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        audio_channel_count=2,
        language_code="en-US")

    # Make API request
    client = speech.SpeechClient()
    response = client.recognize(request={"config": config, "audio": audio})
    detected_text = None
    for result in response.results:
        detected_text = result.alternatives[0].transcript
        print("Transcript: {}".format(result.alternatives[0].transcript))
    return detected_text


# Method for translation
def translate_text(text: str, target_language_code: str) -> translate.Translation:
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        parent=PARENT,
        contents=[text],
        target_language_code=target_language_code,
    )
    return response.translations[0]


# Target Language is a List
def get_translated_text(source_text, target_language):
    try:

            translation = translate_text(source_text, target_language)
            source_language = translation.detected_language_code
            translated_text = translation.translated_text
            # return the translated text from here
            return translated_text
    except Exception as e:
        print(e)
        return -1


"""
Method synthesize_speech_generic Authoreod by : Sanket Bhandari 
"""

def synthesize_speech_generic(text, output_file_location, language_code, voice_name):
    """Synthesizes speech from the input string of text."""

    # Create client object
    client = texttospeech.TextToSpeechClient()

    # Set text input
    input_text = texttospeech.SynthesisInput(text=text)

    # Set voice parameters
    print(voice_name)
    print(language_code)
    if voice_name[-1] == 'A':
        voice = texttospeech.VoiceSelectionParams(
            language_code= str(language_code) , #fr-FR
            name= str(voice_name), #fr-FR-Standard-B
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
    else:
          voice = texttospeech.VoiceSelectionParams(
              language_code= str(language_code) , #fr-FR
              name= str(voice_name), #fr-FR-Standard-B
              ssml_gender=texttospeech.SsmlVoiceGender.MALE,
          )

    # Set audio file format and encoding
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
    )

    # Generate speech
    response = client.synthesize_speech(
        request={
            "input": input_text,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # Write audio to file
    with open(output_file_location, "wb") as out:
        out.write(response.audio_content)

    print(f"Audio content written to file {output_file_location}")


def translate_audio(audio_file, output_translated_audio_location, language_code,voice_name):
    try:
        audio_path = audio_file
        detected_text = extract_text_from_audio(audio_path)
        translated_text = get_translated_text(detected_text, language_code)
        synthesize_speech_generic(translated_text, output_translated_audio_location,language_code,voice_name )
        return True
    except Exception as e:
        print("Exception has occured")
        print(e)
        return  False

def translate_text_only(text_input, output_translated_audio_location, language_code, voice_name):
    try:
        translated_text = get_translated_text(text_input, language_code)
        synthesize_speech_generic(translated_text, output_translated_audio_location,language_code,voice_name )
        return True
    except Exception as e:
        print("Exception has occured")
        print(e)
        return  False
