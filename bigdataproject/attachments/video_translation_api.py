import os
from flask import Flask, request, session, send_from_directory
from werkzeug.utils import secure_filename
# import audio_video_handler

UPLOAD_FOLDER = '/Users/vritansh/Documents/Columbia/EECSFinalSubmission/bigdataproject/converted_videos'
DOWNLOAD_FOLDER = '/home/vk2501/bigdataproject/converted_videos'
import pathlib

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploadImage/<language>', methods=['POST'])
def imageUpload(language):
    target = os.path.join(UPLOAD_FOLDER, 'uploaded')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = pathlib.Path(filename).suffix
    filename = 'uploaded' + extension

    destination = "/".join([target, filename])
    file.save(destination)
    print(language)
    print(request)
    text = request.form.get('text')
    print(text)
    # audio_video_handler.convert_image(language=language.strip(), text_input=text)
    print("success upload .. ")
    return 'success'


@app.route('/upload<language>', methods=['POST'])
def fileUpload(language):
    target = os.path.join(UPLOAD_FOLDER, 'uploaded')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    extension = pathlib.Path(filename).suffix
    filename = 'uploaded' + extension

    destination = "/".join([target, filename])
    file.save(destination)

    session['uploadFilePath'] = destination
    print("covnerting video .. ")
    audio_video_handler.convert_video()
    print("conversion .. completed .. ")
    return 'success'


@app.route('/download')
def get_files():
    try:
        return send_from_directory(DOWNLOAD_FOLDER, 'output.mp4', as_attachment=True)
    except FileNotFoundError:
        return "NO file Found"


@app.route('/test')
def test():
    return 'working'


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, use_reloader=False, port=5500)

flask_cors.CORS(app, expose_headers='Authorization')
