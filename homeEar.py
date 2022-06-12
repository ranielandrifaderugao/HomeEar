import i2clcd
import neopixel
import board

DISPLAY = i2clcd.i2clcd(i2c_bus=4, i2c_addr=0x27, lcd_width=16)
PIXELS = neopixel.NeoPixel(board.D10, 32)
DISPLAY.init()
DISPLAY.print_line('Setting up...', line=0)
PIXELS.fill((0, 0, 0))

import threading
import tensorflow as tf
import numpy as np
import time
import pyaudio
from db import A_weighting, rms
from scipy.signal import lfilter
import librosa
from labels import sound,location
import ctypes
import RPi.GPIO as GPIO
import subprocess

is_location = False #if there is location
set_location_state = False #if picking location or not
set_location = False #setting location or not
set_location_button_state = False #can push set loc button or not
scroll_button_state = False #can push scroll button or not
power_button_state = True
set_power_button_state = False
loc = None
temp = None
location_ctr = 0
reset_temp_ctr = 0
detected = []
NUMERATOR, DENOMINATOR = A_weighting(22050)
WINDOW_LENGTH = int(round(25*22050 / 1000))
HOP_LENGTH = int(round(10*22050 / 1000))
bt = ctypes.CDLL("/home/raspi/homeEar/functions.so")
bt.write_mesh.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int)
bt.read_mesh.argtypes = (ctypes.POINTER(ctypes.c_int),
                         ctypes.POINTER(ctypes.c_char),
                         ctypes.c_int,ctypes.c_int,
                         ctypes.c_int)
f = open('/home/raspi/homeEar/location.txt', 'r')
p = pyaudio.PyAudio()
command = "/usr/bin/sudo /sbin/shutdown -h now"

def button_callback(channel):
    global is_location
    global set_location
    global set_location_state
    global location_ctr
    global scroll_button_state
    global power_button_state
    global set_power_button_state
    if channel == 5 and not is_location and not set_location_state and set_location_button_state:
        is_location = True
    elif channel == 5 and is_location and not set_location_state and set_location_button_state:
        set_location_state = True
        scroll_button_state = True
    elif channel == 5 and is_location and set_location_state and set_location_button_state:
        set_location = True
        set_location_state = False
    elif channel == 25 and scroll_button_state:
        location_ctr+=1
    elif channel == 3 and set_power_button_state:
        stream.stop_stream()
        power_button_state = False
        set_location = False
        set_location_state = False

def locationT():
    global set_location_state
    global set_location
    global location_ctr
    global loc
    global scroll_button_state
    global power_button_state
    while power_button_state:
        time.sleep(0.5)
        if set_location_state:
            stream.stop_stream()
            detected.clear()
            DISPLAY.clear()
            PIXELS.fill((0, 0, 0))
            while set_location_state:
                if location_ctr >= 6:
                    location_ctr = 0
                DISPLAY.print_line('Select location:', line=0)
                DISPLAY.print_line(location[str(location_ctr)]['location'], line=1)
        if set_location:
            file = open("/home/raspi/homeEar/location.txt", "w")
            file.write(str(location_ctr))
            file.close()
            loc = str(location_ctr)
            DISPLAY.clear()
            set_location = False
            scroll_button_state = False
            stream.start_stream()
    
def send(prediction,loc,priority):
    arrSd = ctypes.c_char * 3
    p_send = str.encode(prediction)
    l_send  = str.encode(loc)
    pr_send  = str.encode(priority)
    bt.write_mesh(arrSd(*[p_send ,l_send ,pr_send]),3)
    detected.append((prediction,loc,priority))

def receiveT():
    while bt.read_error() == 0:
        node = ctypes.c_int()
        buf = (ctypes.c_char * 32)()
        x = bt.read_mesh(ctypes.byref(node),buf,ctypes.sizeof(buf),2,0)
        p_receive = buf.value.decode("utf-8")[0]
        l_receive = buf.value.decode("utf-8")[1]
        pr_receive = buf.value.decode("utf-8")[2]
        detected.append((p_receive,l_receive,pr_receive))

def audio_callback(in_data, frame_count, time_info, status_flags):
    global reset_temp_ctr
    global temp
    data = np.frombuffer(in_data, dtype=np.int16) # Convert to [-1.0, +1.0]
    norm_data = (data)/32768.0
    y = lfilter(NUMERATOR, DENOMINATOR, data)
    db = 20*np.log10(rms(y)) + 15
    if db >= 45:
        mels = librosa.feature.melspectrogram(y=norm_data,
                                              sr=22050,
                                              n_fft = WINDOW_LENGTH,
                                              hop_length = HOP_LENGTH,
                                              n_mels= 128)
        mels = librosa.power_to_db(mels)
        mels_min = np.amin(mels)
        mels = (mels-mels_min) / (np.amax(mels)-mels_min)
        mels = np.dstack((mels,mels,mels))
        mels = mels.reshape(1,128,101,3)
        predicted = model.predict(mels)
        prediction = np.argmax(predicted, axis=1)[0]
        probability = predicted[0][prediction] #.99%,.50%
        prediction_str = str(prediction) #0,1,2,3,4,5,6,7,8,9
        priority = sound[prediction_str]['priority'] #0=high,1=med
        if prediction_str not in location[loc]['excluded'] and temp != prediction_str and probability >= .50:
                temp = prediction_str
                if priority == '0':
                    send(prediction_str,loc,priority)
                else:
                    send(prediction_str,loc,priority)
    if reset_temp_ctr > 5:
        temp = None
        reset_temp_ctr = 0
    reset_temp_ctr +=1
    return (in_data, pyaudio.paContinue)

def alert(sound, location, color, i, sleep):
    global set_location_state
    DISPLAY.print_line(sound, line=0)
    DISPLAY.print_line(location, line=1)
    for _ in range(i):
        if set_location_state:
            return
        PIXELS.fill(color)
        time.sleep(sleep)
        PIXELS.fill((0, 0, 0))
        time.sleep(sleep)
    DISPLAY.clear()
    detected.pop(0)

receive_thread = threading.Thread(target=receiveT, daemon=True)
location_thread = threading.Thread(target=locationT, daemon=True)

bt.init()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) #shutdown button
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) #enter button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #scroll button
GPIO.add_event_detect(3,GPIO.RISING,callback=button_callback, bouncetime=500)
GPIO.add_event_detect(5,GPIO.RISING,callback=button_callback, bouncetime=500)
GPIO.add_event_detect(25,GPIO.RISING,callback=button_callback, bouncetime=500)

DISPLAY.print_line('Loading model...', line=0)

model = tf.keras.models.load_model("/home/raspi/homeEar/model/resnet50.hdf5")
model.predict(np.full([1,128,101,3],np.nan))

DISPLAY.clear()

if f.mode=='r':
    content= f.read()
    if content == '':
        while not is_location:
            set_location_button_state = True
            scroll_button_state = True
            if location_ctr >= 6:
                location_ctr = 0
            DISPLAY.print_line('Select location:', line=0)
            DISPLAY.print_line(location[str(location_ctr)]['location'], line=1)
        if is_location:
            file = open("location.txt", "w")
            file.write(str(location_ctr))
            file.close()
            loc = str(location_ctr)
            DISPLAY.clear()
            set_location_button_state = False
            scroll_button_state = False
    else:
        loc = content
        is_location = True

stream = p.open(format=pyaudio.paInt16,
                input_device_index=1,
                channels=1, 
                rate=22050, 
                input=True, 
                frames_per_buffer=22050,
                stream_callback=audio_callback)
receive_thread.start()
location_thread.start()
stream.start_stream()

set_location_button_state = True
set_power_button_state = True

while power_button_state:
    while stream.is_active():
        if detected:
            detected.sort(key=lambda x: (x[2]))
            latest_sound = detected[0][0]
            latest_loc = detected[0][1]
            prio = detected[0][2]
            if prio =='0' :
                alert(sound[latest_sound]['sound'],
                      location[latest_loc]['location'],
                      sound[latest_sound]['color'],
                      15,
                      0.1)
            else:
                alert(sound[latest_sound]['sound'],
                      location[latest_loc]['location'],
                      sound[latest_sound]['color'],
                      3,
                      0.55)
                
#shutdown rasperry pi
stream.close()
p.terminate()
bt.close_all()
PIXELS.fill((0, 0, 0))
DISPLAY.clear()
DISPLAY.print_line('Wait a moment to', line=0)
DISPLAY.print_line('unplug/restart', line=1)
time.sleep(2)
DISPLAY.clear()
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]