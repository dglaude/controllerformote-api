from colorsys import hsv_to_rgb, rgb_to_hsv
import apa
from flask import Flask, jsonify, make_response

app = Flask(__name__)

numleds = 8    # number of LEDs in our display

brightness = 0xE2

ledstrip = apa.Apa(numleds)

ledstrip.flush_leds()
ledstrip.zero_leds()
ledstrip.write_leds()

colour = 'FFFFFF'
status = 0

def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))

def inspiring_on(c):
    r, g, b = hex_to_rgb(c)
    for pixel in range(numleds):
        ledstrip.led_set(pixel, brightness, b, g, r)
    ledstrip.write_leds()
    return True

def inspiring_off():
    global status
    ledstrip.zero_leds()
    ledstrip.write_leds()
    status=0
    return True

def get_status():
    global status
    return status

@app.route('/mote/api/v1.0/<string:st>', methods=['GET'])
def set_status(st):
    global status, colour
    if st == 'on':
        status = 1
        inspiring_on(colour)
    elif st == 'off':
        status = 0
        inspiring_off()
    elif st == 'status':
        status = get_status()
    return jsonify({'status': status, 'colour': colour})

@app.route('/mote/api/v1.0/set', methods=['GET'])
def get_colour():
    global colour
    return jsonify({'status': status, 'colour': colour})

@app.route('/mote/api/v1.0/set/<string:c>', methods=['GET'])
def set_colour(c):
    global status, colour
    colour = c
    if status != 0:
        inspiring_on(colour)
        status = 1
    return jsonify({'status': status, 'colour': colour})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    inspiring_off()
    app.run(host='0.0.0.0', debug=True)

