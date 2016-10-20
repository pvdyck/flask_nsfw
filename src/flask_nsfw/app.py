#!/usr/bin/env python2

from sys import stdout, exc_info
from os import remove
from time import time
from warnings import warn
from traceback import format_exc, print_exc

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from open_nsfw import classify_nsfw

app = Flask(__name__)

class NoSubmission (Exception):
    status_code = 400
    message = 'No image submitted'

class StorageError (Exception):
    status_code = 500
    message = 'Storage error'

class InvalidSubmission (Exception):
    status_code = 400
    message = 'Could not process image'

class ClassificationError (Exception):
    status_code = 500
    message = 'Classification error'

def save (key):
    # ignore missing files
    if key not in request.files or not request.files[key].filename:
        return None, None
    f = request.files[key]

    # timestamp, discard extension, save to temp dir
    name = str(int(time() * 1000000))
    path = '/tmp/' + name
    try:
        f.save(path)
    except:
        try:
            remove(path)
        except:
            pass
        raise StorageError()

    return path, name

def delete (f):
    try:
        remove(f)
    except:
        warn("could not delete " + f, RuntimeWarning)

def classify ():
    # save image
    img = save('image')
    if img[0] is None:
        raise NoSubmission()

    # validate image
    try:
        im = Image.open(img[0])
    except:
        delete(img[0])
        raise InvalidSubmission()

    # save custom models if present
    model_def = save('model_def')
    pretrained_model = save('pretrained_model')

    # classify image
    try:
        score = classify_nsfw.classify(img[0], model_def[0], pretrained_model[0])
    except:
        raise ClassificationError()

    # clean up and return classification results
    delete(img[0])
    return { 'image': img[1], 'score': score[1] }
 
@app.route('/', methods=['GET', 'POST'])
def index ():
    if request.method == 'POST':
        return jsonify(repr(classify()['score']))
    return render_template('index.html')

@app.errorhandler(Exception)
def on_error (error):
    status_code = getattr(error, 'status_code', 500)
    response = {
        "status_code": status_code,
        "message": getattr(error, 'message', 'Error'),
        "traceback": format_exc()
    }
    print response
    response = jsonify(response)
    response.status_code = status_code
    print_exc(file=stdout)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
