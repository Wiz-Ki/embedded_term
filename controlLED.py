import RPi.GPIO as GPIO

def init_led():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    GPIO.output(2, GPIO.LOW)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, GPIO.LOW)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)
# LED 제어 함수
def control_led(device, action):
    init_led()

    if action == 'turn_on':
        if device == 'airconditioner':
            pin = 2
            GPIO.output(pin, GPIO.HIGH)
        elif device == 'heater':
            pin = 3
            GPIO.output(pin, GPIO.HIGH)
        elif device == 'lights':
            pin = 4
            GPIO.output(pin, GPIO.HIGH)
        elif device == 'tv':
            pin = 17
            GPIO.output(pin, GPIO.HIGH)
    elif action == 'turn_off':
        if device == 'airconditioner':
            pin = 2
            GPIO.output(pin, GPIO.LOW)
        elif device == 'heater':
            pin = 3
            GPIO.output(pin, GPIO.LOW)
        elif device == 'lights':
            pin = 4
            GPIO.output(pin, GPIO.LOW)
        elif device == 'tv':
            pin = 17
            GPIO.output(pin, GPIO.LOW)
    else:
        return

