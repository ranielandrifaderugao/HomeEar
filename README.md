# HomeEar: AN IN-HOME AWARENESS AND ALERTING SYSTEM FOR THE DEAF AND HARD-OF-HEARING

HomeEar is designed as a system of devices that will serve as a companion for the deaf and hard-of-hearing people inside their homes. Its primary function is to recognize important sounds present at home and alert them right away. 

The system is divided into four processes. These are capture audio, compute features, model prediction, and network. To use this in your Raspberry Pi you will need to do the following:

## CAPTURE AUDIO
For the microphone, we used [inmp441](https://makersportal.com/shop/i2s-mems-microphone-for-raspberry-pi-inmp441) mems microphone. Install the module for [microphone](https://makersportal.com/blog/recording-stereo-audio-on-a-raspberry-pi). We used a sampling rate of 22.5 kHz and we capture audio for every one second.

## COMPUTE FEATURES


1. Clone the repository for the [bluetooth interface](https://github.com/petzval/btferret) of Rasperry Pi. This is used to send the sounds detected by one device to other devices.
2. Install the module for the [LCD](https://github.com/WuSiYu/python-i2clcd). When installing the LCD on the Raspberry Pi make use of other pins using this [configuration](https://www.instructables.com/Raspberry-PI-Multiple-I2c-Devices/). This is used to display the location and the sound detected.
3. 
4. Install the module for [LED](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage). 
5. In this project we used a resnet50 model for audio classification. It is possible to use other model like densenet model or other resnet model. We used an input shape of (1,128,101,3) to feed into the model. 
dawds
