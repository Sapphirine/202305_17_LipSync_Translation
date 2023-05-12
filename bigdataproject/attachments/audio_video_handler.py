import inference_inject_static
import extract_audio_from_video
import automated_transcription_script
import os

CHECKPOINT_PATH = "/content/bigdataproject/Wav2Lip/checkpoints/wav2lip.pth"
FINAL_OUTPUT_DIRECTOR = "/content/bigdataproject/converted_videos/output.mp4"
OUTPUT_TRANSLATED_AUDIO_LOCATION = "/content/bigdataproject/translated_audio/translated.wav"
OUTPUT_AUDIO_FILE_LOCATION="/content/bigdataproject/extracted_audio"
DEFAULT_VIDEO_FILE ="/content/sample_data/talk_voice_English.mp4"
DEFAULT_VIDEO_FILE_NAME ="talk_voice_English"
DEFAULT_LANGAUGE = "Mandarin"

# Interaction method with the actual Wav2Lip model
def get_conversions(audio_file, video_file, file_name, final_output_directory):
    try:
            checkpoint_path = CHECKPOINT_PATH
            inference.get_conversion(audio_file, video_file,  file_name,  checkpoint_path, final_output_directory)

    except Exception as e:
        print("Exception has occured.. get_conversion")
        print(e)
        return False
    return True

# for finding langauge code
def find_language_code(language):
    langcode_audio = {
                      'English': 'en-EN',
                      'Hindi': 'hi-IN',
                      'Hindi_female': 'hi-IN',
                      'Mandarin': 'cmn-CN',
                      'Mandarin_female': 'cmn-CN',
                      'Spanish': 'es-ES',
                      'Spanish_female': 'es-ES',
                      'French': 'fr-FR',
                      'French_female': 'fr-FR',
                      'German':'de-DE',
                      'German_female':'de-DE'
                      }

    voice_name = {

        'Hindi': 'hi-IN-Standard-B',
        'Hindi_female': 'hi-IN-Standard-A',
        'Mandarin': 'cmn-CN-Standard-B',
        'Mandarin_female': 'cmn-CN-Standard-A',
        'Spanish': 'es-ES-Standard-B',
        'Spanish_female': 'es-ES-Standard-A',
        'French': 'fr-FR-Standard-B',
        'French_female': 'fr-FR-Standard-A',
        'German': 'de-DE-Standard-B',
        'German_female': 'de-DE-Standard-A'

    }
    return langcode_audio[language], voice_name[language]

# Pass on the language from  GCP codec

def convert_video(video_file=DEFAULT_VIDEO_FILE, output_audio_file_location=OUTPUT_AUDIO_FILE_LOCATION, output_translated_audio_location=OUTPUT_TRANSLATED_AUDIO_LOCATION, video_file_name=DEFAULT_VIDEO_FILE_NAME , language=DEFAULT_LANGAUGE, final_output_directory=FINAL_OUTPUT_DIRECTOR):
    try:
        language_code, voice_name = find_language_code(language)
        video_file_name = video_file_name + "_" +language
        audio_file_id = "/" + video_file_name +".wav"
        output_audio_file_location = output_audio_file_location + audio_file_id
        extract_audio_from_video.extract_audio(video_file, output_audio_location=output_audio_file_location)
        transation_completed = automated_transcription_script.translate_audio(output_audio_file_location,
                                                                              output_translated_audio_location,
                                                                              language_code=language_code,
                                                                              voice_name = voice_name
                                                                              )
        if transation_completed:
            get_conversions(output_translated_audio_location, video_file, video_file_name, final_output_directory)
        return True
    except Exception as e:
        print("Exception has occured ...  convert_video() ")
        print(e)
        
        return False


def convert_image(video_file=DEFAULT_IMAGE_FILE, output_audio_file_location=OUTPUT_AUDIO_FILE_LOCATION, output_translated_audio_location=OUTPUT_TRANSLATED_AUDIO_LOCATION, video_file_name=DEFAULT_VIDEO_FILE_NAME , language=DEFAULT_LANGAUGE, final_output_directory=FINAL_OUTPUT_DIRECTOR, text_input='Hello'):
    try:
        print("Using convert image...")
        print(text_input)
        language_code, voice_name = find_language_code(language)
        print("fetched langauge code ...")
        video_file_name = video_file_name + "_" +language
        audio_file_id = "/" + video_file_name +".wav"
        output_audio_file_location = output_audio_file_location + audio_file_id
#         extract_audio_from_video.extract_audio(video_file, output_audio_location=output_audio_file_location)
        transation_completed = automated_transcription_script.translate_text_only(text_input,
                                                                              output_translated_audio_location,
                                                                              language_code=language_code,
                                                                              voice_name = voice_name
                                                                              )
        if transation_completed:
            get_conversions(output_translated_audio_location, video_file, video_file_name, final_output_directory)
        return True
    except Exception as e:
        print("Exception has occured ...  convert_image() ")
        print(e)
        return False


def test_all_videos():

    # specify the path of the directory to read it should be arranged as described in deployment doc
    directory_path = "/content/drive/MyDrive/BigDataProject/downloaded_video"
    # Below are native to your folders
    converted_videos_path = '/content/bigdataproject/converted_videos'
    output_audio_file_location="/content/bigdataproject/extracted_audio"
    output_translated_audio_location="/content/bigdataproject/translated_audio/translated.wav"
    # Currenlty update the language from a list of available languages.
    language = "Hindi"

    # use the listdir method to get a list of all the files and directories in the specified directory
    directory_contents = os.listdir(directory_path)

    for content in directory_contents:
        
        if  os.path.isdir(os.path.join(directory_path, content)):

            # Creating final video folder here
            new_directory_name = content
            final_output_directory = os.path.join(converted_videos_path, new_directory_name)
            os.makedirs(final_output_directory, exist_ok=True)
            file_list = os.listdir(os.path.join(directory_path, content))
            
            if content[8:] == 'female':
               language_new = language+"_"+"female"
            else:
              language_new = language
            for f in file_list:
                input_video_file = os.path.join(directory_path, content, f)
                final_output_directory_new = os.path.join(final_output_directory, f)
                # print(f"   File: {file_path}")
                video_file_name = f[:-4]
                print(final_output_directory_new)
                convert_video(input_video_file, output_audio_file_location, output_translated_audio_location,
                              video_file_name, language_new, final_output_directory_new)
                # return
                # convert_video(video_file, output_audio_file_location, output_translated_audio_location, video_file_name , language, final_output_directory):

# Uncomment below for generating samples from a large corpus

# if __name__ == '__main__':
#     test_all_videos()
