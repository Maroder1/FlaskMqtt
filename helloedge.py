"""

SIMATIC Edge test application using Flask and MQTT

"""

import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import os


eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = os.environ.get('SECRET_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_URL'] = os.environ.get('MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.environ.get('MQTT_BROKER_PORT'))
app.config['MQTT_USERNAME'] = os.environ.get('MQTT_USERNAME')
app.config['MQTT_PASSWORD'] = os.environ.get('MQTT_PASSWORD')
app.config['MQTT_KEEPALIVE'] = int(os.environ.get('MQTT_KEEPALIVE'))
app.config['MQTT_TLS_ENABLED'] = False

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'], data['qos'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'], data['qos'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        qos=message.qos,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


@mqtt.on_disconnect()
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)