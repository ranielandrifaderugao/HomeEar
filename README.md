# HomeEar: AN IN-HOME AWARENESS AND ALERTING SYSTEM FOR THE DEAF AND HARD-OF-HEARING

HomeEar is designed as a system of devices that will serve as a companion for the deaf and hard-of-hearing people inside their homes. Its primary function is to recognize important sounds present at home and alert them right away.

To use this in your Raspberry Pi you will need to do the following:
1. Clone the repository for the [bluetooth interface](https://github.com/petzval/btferret) of Rasperry Pi.
2. Install the module for the [LCD](https://github.com/WuSiYu/python-i2clcd). When installing the LCD on the Raspberry Pi make use of other pins using this [configuration](https://www.instructables.com/Raspberry-PI-Multiple-I2c-Devices/).
3. Install the module for [microphone](https://makersportal.com/blog/recording-stereo-audio-on-a-raspberry-pi).
4. Install the module for [LED](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage). 
5. Use a resnet50 model for audio classification.
