import random
from flask import (
    Blueprint, render_template, jsonify
)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='BotanicPet')

@bp.route('/camera')
def camera():
    return render_template('main/camera.html',
                           title='BotanicPet')

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
