# Libraries and GPIO Setup -------------------------------------------- {{{

import glob
import os
import sys
import thread
import time
import urllib2

import RPi.GPIO as io

import tweet

io.setmode(io.BOARD)

# }}}
# Global Variables -------------------------------------------------- {{{

previous_temp = None
current_color = "white"
temp_sequence = []
temp_status = "normal"
last_tweet_check = time.time()
tweet_check_count = 0
connection_failures = 0

# }}}
# Temp Sensing -------------------------------------------------- {{{

# read_temp -------------------------------------------------- {{{

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"

def read_temp():
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()

    equals_pos = lines[1].find("t=")

    if equals_pos != 1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 33
        return temp_f
    else:
        return False

# }}}
# convert_temp_to_constant ------------------------------------------ {{{

REALLY_COLD, COLD, NORMAL, HOT, REALLY_HOT = (2, 3, 4, 5 ,6)

def convert_temp_to_constant(temp_float):
    if temp_float > 90:
        return REALLY_HOT
    elif temp_float > 80:
        return HOT
    elif temp_float > 50:
        return NORMAL
    elif temp_float > 32:
        return COLD
    else:
        return REALLY_COLD

# }}}
# temp_sequence_check ------------------------------------------------ {{{

def temp_sequence_check(temp_constant):
    result = False
    if temp_constant not in temp_sequence:
        result = True
    if len(temp_sequence) > 5:
        temp_sequence.pop(0)
    temp_sequence.append(temp_constant)
    return result

# }}}

def set_led_to_current_temp(temp_constant):
    global current_color
    if temp_constant == REALLY_HOT:
        current_color = "red"
    elif temp_constant == HOT:
        current_color = "yellow"
    elif temp_constant == NORMAL:
        current_color = "green"
    elif temp_constant == COLD:
        current_color = "cyan"
    elif temp_constant == REALLY_COLD:
        current_color = "blue"

def handle_temp_reading(temp):
    working_temp = convert_temp_to_constant(temp)
    set_led_to_current_temp(working_temp)
    if temp_sequence_check(working_temp):
        if working_temp == REALLY_HOT:
            temp_change_tweet("Holy cow it's really hot in here! My leaves are starting to burn!")
        elif working_temp == HOT:
            temp_change_tweet("Man I'm starting to sweat in here!")
        elif working_temp == NORMAL:
            temp_change_tweet("Looks like everything is back to normal.")
        elif working_temp == COLD:
            temp_change_tweet("Brr.. it's getting colder in here!")
        elif working_temp == REALLY_COLD:
            temp_change_tweet("Come on turn up the heat, I'm freezin my ass off in here!")

# }}}
# LED Setup and Control ---------------------------------------------- {{{

RGB_RED = 16 # 23
RGB_GREEN = 18 # 24
RGB_BLUE = 22 # 25

RGB = {"red": RGB_RED, "green": RGB_GREEN, "blue": RGB_BLUE}

red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
white = [1, 1, 1]
yellow = [1, 1, 0]
cyan = [0, 1, 1]
purple = [1, 0, 1]

colors = {"red": red, "green": green, "blue": blue, "white": white, "yellow": yellow, "cyan": cyan, "purple": purple}

def rgb_setup():
    for val in RGB:
        io.setup(RGB[val], io.OUT)

def rgb_pulse(rgb_led, color, speed, lower_limit):
    r = io.PWM(rgb_led["red"], 50)
    g = io.PWM(rgb_led["green"], 50)
    b = io.PWM(rgb_led["blue"], 50)

    r.start(0)
    g.start(0)
    b.start(0)

    if color not in colors.values():
        raise ValueError("Please enter a valid color")

    try:
        while True:
            for i in range(lower_limit, 100):
                r.ChangeDutyCycle(i * color[0])
                g.ChangeDutyCycle(i * color[1])
                b.ChangeDutyCycle(i * color[2])
                time.sleep(speed)
            for i in range(100, lower_limit, -1):
                r.ChangeDutyCycle(i * color[0])
                g.ChangeDutyCycle(i * color[1])
                b.ChangeDutyCycle(i * color[2])
                time.sleep(speed)

    except KeyboardInterrupt:
        pass

    r.stop()
    g.stop()
    b.stop()

# }}}
# WiFi Functions -------------------------------------------------- {{{

def check_internet_connection():
    global connection_failures
    global last_tweet_check
    instance_connection_failures = 0
    if time.time() - last_tweet_check > 60:
        try:
            # os.popen("ping -c 5 192.168.0.2")
            urllib2.urlopen("http://192.186.0.2", timeout=1)
        except urllib2.URLError as err:
            print err
            print "Unable to ping wifi!"
            instance_connection_failures += 1
            pass

        try:
            # os.popen("ping -c 3 www.twitter.com")
            urllib2.urlopen("http://www.twitter.com", timeout=1)
        except urllib2.URLError as err:
            print err
            print "Unable to ping twitter! @ %s" % time.ctime()
            instance_connection_failures += 1
            pass
        last_tweet_check = time.time()

    if instance_connection_failures > 0:
        connection_failures += 1
        if connection_failures > 2:
            reboot()
    else:
        connection_failures = 0

# }}}
# Tweeting Functions -------------------------------------------------- {{{

last_temp_tweet = [time.time()]

def temp_change_tweet(message):
    if time.time() - last_temp_tweet[0] > 300:
        tweet.tweet(message)
        last_temp_tweet[0] = time.time()

def check_tweets(current_temp):
    try:
        thread.start_new_thread(tweet.temp_request, (current_temp,))
        print "The tweet check count is:", tweet_check_count
        last_tweet_check = time.time()
        tweet_check_count += 2
    except:
        print "There was a problem with threading!"
        pass

# }}}
# Graphing Functions -------------------------------------------------- {{{

def write_last_24_hour_graph_render():
    f = open("last_24_hour_graph_render.txt", "w")
    f.write(str(time.time()))
    f.close()

def get_last_24_hour_graph_render():
    f = open("last_24_hour_graph_render.txt")
    return float(f.read())

def write_last_7_days_graph_render():
    f = open("last_7_days_graph_render.txt", "w")
    f.write(str(time.time()))
    f.close()

def get_last_7_days_graph_render():
    f = open("last_7_days_graph_render.txt", "w")
    return float(f.read())

# }}}
# Helper Functions -------------------------------------------------- {{{

def reboot():
    print "Rebooting!"
    os.popen("reboot");
    raise Exception

# }}}
# Main Loop -------------------------------------------------- {{{

# RGB LED Setup -------------------------------------------------- {{{

rgb_setup()

r = io.PWM(RGB["red"], 50)
g = io.PWM(RGB["green"], 50)
b = io.PWM(RGB["blue"], 50)

r.start(0)
g.start(0)
b.start(0)

def clear_led():
    r.ChangeDutyCycle(0)
    g.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)

def pulse_up():
    color = colors[current_color]
    for i in range(100):
        r.ChangeDutyCycle(i * color[0])
        g.ChangeDutyCycle(i * color[1])
        b.ChangeDutyCycle(i * color[2])
        time.sleep(0.02)

def pulse_down():
    color = colors[current_color]
    for i in range (100, 1, -1):
        r.ChangeDutyCycle(i * color[0])
        g.ChangeDutyCycle(i * color[1])
        b.ChangeDutyCycle(i * color[2])
        time.sleep(0.02)

# }}}

while True:
    try:
        # Sequence of events
        # 1. Clear led? is this necessary?
        clear_led()
        # 2. Pulse led high to color from previous temp reading
        pulse_up()
        # for i in range(100):
        #     r.ChangeDutyCycle(i * color[0])
        #     g.ChangeDutyCycle(i * color[1])
        #     b.ChangeDutyCycle(i * color[2])
        #     time.sleep(0.02)
        # 3. Read temp
        current_temp = read_temp()
        # 4. Check and handle wifi
        check_internet_connection()
        # 5. Handle temp reading, tweet if necessary
        handle_temp_reading(current_temp)
        # 6. Check tweets for temp request
        # check_tweets(current_temp)
        # 7. See if a graph needs to be drawn, draw and tweet if necessary
        #TODO
        # 8. Pulse led low
        pulse_down()
        # color = colors[current_color]
        # for i in range (100, 1, -1):
        #     r.ChangeDutyCycle(i * color[0])
        #     g.ChangeDutyCycle(i * color[1])
        #     b.ChangeDutyCycle(i * color[2])
        #     time.sleep(0.02)
        # 9. Repeat

        # r.ChangeDutyCycle(0)
        # g.ChangeDutyCycle(0)
        # b.ChangeDutyCycle(0)

        # temp_reading = read_temp()
        # # Handle temp reading
        # if temp_reading:
        #     if temp_reading >= 90:
        #         current_color = "red"
        #         if temp_status != "really hot":
        #             temp_change_tweet("Holy cow it's really hot in here! My leaves are starting to burn!")
        #             temp_status = "really hot"
        #     elif temp_reading >= 80:
        #         current_color = "yellow"
        #         if temp_status != "hot":
        #             temp_change_tweet("Man I'm starting to sweat in here!")
        #             temp_status = "hot"
        #     elif temp_reading >= 50:
        #         current_color = "green"
        #         if temp_status != "normal":
        #             temp_change_tweet("Looks like everything is back to normal.")
        #             temp_status = "normal"
        #     elif temp_reading >= 32:
        #         current_color = "cyan"
        #         if temp_status != "cold":
        #             temp_change_tweet("Brr.. it's getting colder in here!")
        #             temp_status = "cold"
        #     else:
        #         current_color = "blue"
        #         if temp_status != "really cold":
        #             temp_change_tweet("Come on turn up the heat, I'm freezin my ass off in here!")
        #             temp_status = "really_cold"

        #     previous_temp = temp_reading
        # else:
        #     print previous_temp

        # # Check Wi-fi and Internet connection
        # # Check if temp requested tweet if necessary


        # # One Minute Time Check
        # if time.time() - last_tweet_check > 60:

        #     try:
        #         os.popen("ping -c 5 192.168.0.2")
        #     except:
        #         print "Unable to ping wifi!"
        #         pass

        #                 try:
        #         os.popen("ping -c 3 www.google.com")
        #     except:
        #         print "Unable to ping google! @ %s" % time.ctime()
        #         pass

        #     # try:
        #     #     ifconfig = os.popen("ifconfig wlan0")
        #     #     if "inet addr:" not in ifconfig.read():
        #     #         print "Forcing connection to wifi, I hope this works @ %s" % time.ctime()
        #     #         try:
        #     #             force_wifi_shutdown = os.popen("ifdown --force wlan0")
        #     #             print "Shutting down wifi connection @ %s" % time.ctime()
        #     #             time.sleep(10)
        #     #             print "Reconnecting wifi connection @ %s" % time.ctime()
        #     #             force_wifi_reconnection = os.popen("ifup --force wlan0")
        #     #             print "Wifi reconnection said: %s" % force_wifi_reconnection.read()
        #     #         except Exception, e:
        #     #             print "Unable to force wifi connection. @ %s" % time.ctime()
        #     #             print "Wifi reconnection error: %s" % e
        #     #             pass

        #     # except:
        #     #     print "There was a problem retrieving ifconfig for wlan0 @ %s" % time.ctime()
        #     #     pass

        #     try:
        #         thread.start_new_thread(tweet.temp_request, (temp_reading,))
        #         print "The tweet check count is:", tweet_check_count
        #         last_tweet_check = time.time()
        #         tweet_check_count += 2
        #     except:
        #         print "There was a problem with threading!"
        #         pass


        # for i in range(100):
        #     color = colors[current_color]
        #     if switch_status:
        #         r.ChangeDutyCycle(i * color[0])
        #         g.ChangeDutyCycle(i * color[1])
        #         b.ChangeDutyCycle(i * color[2])
        #     time.sleep(0.02)

        # for i in range (100, 1, -1):
        #     color = colors[current_color]
        #     if switch_status:
        #         r.ChangeDutyCycle(i * color[0])
        #         g.ChangeDutyCycle(i * color[1])
        #         b.ChangeDutyCycle(i * color[2])
        #     time.sleep(0.02)

        # # Forcing stdout to write
        sys.stdout.flush()

    except Exception, e:
        print e
        print "The script was stopped."
        io.cleanup()
        sys.exit(1)

        r.stop()
        g.stop()
        b.stop()

# }}}
