# HomeEar: AN IN-HOME AWARENESS AND ALERTING SYSTEM FOR THE DEAF AND HARD-OF-HEARING

![HomeEar](https://user-images.githubusercontent.com/63916644/173497158-d913cbd4-3b5d-4268-8069-9864439469c7.png)

HomeEar is designed as a system of devices that will serve as a companion for the deaf and hard-of-hearing people inside their homes. Its primary function is to recognize essential sounds at home and alert them immediately. It supports seven sounds and has six locations selection.

The system is divided into four processes. These are capture audio, compute features, model prediction, and network.

## CAPTURE AUDIO
[inmp441](https://makersportal.com/shop/i2s-mems-microphone-for-raspberry-pi-inmp441) mems microphone is used as the capturing device. Install the module for [microphone](https://makersportal.com/blog/recording-stereo-audio-on-a-raspberry-pi). A sampling rate of 22.5 kHz is used, and the microphone captured audio for every second using PyAudio library.
  
## COMPUTE FEATURES
A single Mel-Spectrogram computed using a window size of 25ms and hop length of 10ms is replicated across the three channels. The shape that is created should be (128,101,3). It is then fed into the audio classification model. 
  
## MODEL PREDICTION
A resnet50 model is used for audio classification. Using another model like the densenet model or other resnet models is possible. The input shape to be fed into the model should be in the shape of (1,128,101,3). 

## NETWORK
The network process consists of the system's communication and alerting function. For the communication, clone the repository for the [bluetooth interface](https://github.com/petzval/btferret) of Raspberry Pi. This is used to send the sounds detected by one device to other devices. Note that the Bluetooth interface used is in the language of C, and the system is developed using python. In order to use it, ctypes library is used. For the alerting function, Install the module for the [LCD](https://github.com/WuSiYu/python-i2clcd). This is used to display the location, and the sound detected. When installing the LCD on the Raspberry Pi, make use of other pins using this [configuration](https://www.instructables.com/Raspberry-PI-Multiple-I2c-Devices/) because the i2c pin is used for shutdown function. Install the module for [LED](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage). This is used for visual alert. The colors can be changed using the labels.py file.

