import BlynkLib, requests, sendAlarmToFirebase
from sense_hat import SenseHat, ACTION_PRESSED
from time import sleep

# Configuring Blynk & SenseHAT
BLYNK_AUTH = 'fZ5ulMaDTC9OO1T2-qDtEaoVHmF2wlfw'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
sense = SenseHat()
sense.clear()
sense.color.gain = 64
sense.color.integration_cycles = 256

# Pixel array variables

G = [0, 191, 75]   # Green
B = [75, 75, 191]  # Blue
P = [162, 0, 162]  # Purple
N = [0, 0, 0]      # No light

pixel_array = [
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N,
N, N, N, N, N, N, N, N ]

# Stores pixel locations as they move across the light array
pixel = 0
# Instead of sending data to Blynk every 0.05s, this iterating variable allows data to be sent every 0.5s
readings = 0
# Flag to break out of sub-function loops. Reset to zero with each loop of the main loop
breakout = 0
# Flag for whether alarm is armed
armed = 0
# Flag for alarm state
alarm = 0

# Sends a HTTPS GET request to Blynk to trigger an event
def https_event(event):
    get_request = requests.get(f'https://blynk.cloud/external/api/logEvent?token={BLYNK_AUTH}&code={event}')
    print (get_request)

# Register handler for Blynk app Alarm state toggle
@blynk.on("V0")
def v0_write_handler(value):
    global alarm
    global armed
    global breakout
    if alarm == 1:
        alarm = value[0]
        armed = value[0]
        breakout = 1
        https_event("alarm_disarmed")

# Register handler for Blynk app Armed state toggle
@blynk.on("V2")
def v2_write_handler(value):
    global armed
    armed = value[0]
    https_event("alarm_armed")


# Toggles off the alarm if three sequential joystick input events are all correct - down up down - otherwise breaks out.
def toggle_off_check():

    # Layer 1: Check once for joystick pressed 'down'
    for x in sense.stick.get_events():
        if x.direction == "down" and x.action == "pressed":
            global breakout
            global armed
            global alarm
            continue_ = 0
            sense.set_pixel(6, 7, 0, 85, 170)
            while True:

        	# Layer 2: Wait and check for joystick pressed 'up'
                if breakout == 1 or continue_ == 1:
                    break
                for x in sense.stick.get_events():
                    if x.direction != "up" and x.action == "pressed":
                        continue_ = 1
                    elif x.direction == "up" and x.action == "pressed":
                        sense.set_pixel(7, 7, 0, 0, 255)
                        while True:

                            # Layer 3: Wait and check for joystick pressed 'down'
                            if breakout == 1 or continue_ == 1:
                                break
                            for y in sense.stick.get_events():
                                if y.direction != "down" and y.action == "pressed":
                                    continue_ = 1
                                elif y.direction == "down" and y.action == "pressed":
                                    sense.show_letter("O", text_colour=[0, 0, 255])
                                    sleep(0.2)
                                    sense.show_letter("K", text_colour=[0, 0, 255])
                                    sleep(0.2)
                                    sense.clear()
                                    sleep(0.2)
                                    armed = 0
                                    alarm = 0
                                    blynk.run()
                                    blynk.virtual_write(0, alarm)
                                    blynk.virtual_write(2, armed)
                                    https_event("alarm_disarmed")
                                    breakout = 1

# Toggles on the alarm if three sequential joystick input events are all correct - up down up - otherwise breaks out.
def toggle_on_check():

    # Layer 1: Check once for joystick pressed 'up'
    for x in sense.stick.get_events():
        if x.direction == "up" and x.action == "pressed":
            global breakout
            global armed
            global light
            sense.set_pixel(6, 7, 170, 85, 0)
            while True:

        	# Layer 2: Wait and check for joystick pressed 'down'
                if breakout == 1:
                    break
                for x in sense.stick.get_events():
                    if x.direction != "down" and x.action == "pressed":
                        breakout = 1
                    elif x.direction == "down" and x.action == "pressed":
                        sense.set_pixel(7, 7, 255, 0, 0)
                        while True:

                            # Layer 3: Wait and check for joystick pressed 'up'
                            if breakout == 1:
                                break
                            for y in sense.stick.get_events():
                                if y.direction != "up" and y.action == "pressed":
                                    breakout = 1
                                elif y.direction == "up" and y.action == "pressed":
                                    sense.show_message("Arming        ", scroll_speed = 0.080, text_colour=[255, 0, 0])
                                    armed = 1
                                    blynk.run()
                                    blynk.virtual_write(2, armed)
                                    https_event("alarm_armed")
                                    light = sense.colour.colour[3]
                                    light_check()
                                    breakout = 1

# Function that checks light levels. If above '5', triggers the alarm state & pushes data to Blynk & Firebase
def light_check():
    uploadCounter = 1
    global breakout
    global alarm
    global light
    if light > 5:
        countdown = 5
        alternator = 0
        while True:
            toggle_off_check()
            if breakout == 1:
                break
            if alternator == 0:
                sense.show_letter("!", text_colour=[255, 128, 0])
                alternator += 1
            else:
                sense.clear()
                alternator -= 1
            sleep(0.6)
            countdown -= 1
            if countdown <= 0:
                while True:
                    alarm = 1
                    if uploadCounter == 1:
                        blynk.run()
                        blynk.virtual_write(0, alarm)
                        https_event("alarm")
                        sendAlarmToFirebase.alarm_event()
                        uploadCounter = 0
                    toggle_off_check()
                    blynk.run()
                    if breakout == 1:
                        break
                    if alternator == 0:
                        sense.show_message("! ! !", scroll_speed = 0.05, text_colour=[255, 85, 0])
                        alternator += 1
                    else:
                        sense.show_message("! ! !", scroll_speed = 0.05, text_colour=[0, 0, 0], back_colour = [255, 85, 0])
                        alternator -= 1

while True:
    toggle_on_check()

    # Iterates lit and unlit pixels across the light array
    pixel += 1
    if pixel > 27:
        pixel = 0
    pixel_array[pixel - 3] = N
    if pixel < 24:
        if pixel > 1:
            pixel_array[pixel - 2] = P
        if pixel > 0:
            pixel_array[pixel - 1] = B
        pixel_array[pixel] = G
    sense.set_pixels(pixel_array)

    readings += 1
    if readings > 9:
        light = sense.colour.colour[3]
        print(f"Light: {light}")
        if armed == "1":
            light_check()
        blynk.run()
        blynk.virtual_write(0, alarm)
        blynk.virtual_write(1, light)
        blynk.virtual_write(2, armed)
        readings = 0

    breakout = 0
    sleep(0.05)
