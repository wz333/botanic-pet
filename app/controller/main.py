import random
from importlib import import_module
from flask import (
    Blueprint, render_template, jsonify, Response
)
import sys
import os
sys.path.append(os.path.dirname(__file__))

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='BotanicPet')
                        

@bp.route('/camera')
def camera():
    return render_template('main/camera.html',
                           title='BotanicPet')
def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@bp.route('/chat')
def chat():
    return render_template('main/chat.html',
                           title='BotanicPet')

@bp.route('/pet_status')
def pet_status():
    status_code=None
    status_code=random.choice(['00', '03', '03','03','04'])
    data="{{url_for('static', filename='images/emojis/{}.gif')}}".format(status_code)

    return jsonify({'data':status_code})
    # return status_code

@bp.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

