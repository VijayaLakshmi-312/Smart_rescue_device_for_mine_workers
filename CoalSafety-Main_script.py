import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_ADS1x15
import playsound

dustPin = 3;
ledPin = 4;
Tsampling = 280;
Tdelta = 40;
Tsleep = 9680;
outVo = 0.0;
sigVolt = 0.0;
dustLevel = 0.0;
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
print("\n#########################################\nWelcome to Coal Mine Safety Device\n#########################################")
#playsound('Soundrec/start.wav');
while True:
    GPIO.output(ledPin, GPIO.LOW)
   
    time.sleep(Tsampling/1000000)

    outVo = adc.read_adc(dustPin, gain=GAIN);

    time.sleep(Tdelta/1000000)

    GPIO.output(ledPin, GPIO.HIGH)
   
    time.sleep(Tsleep/1000000)

    sigVolt = outVo * (4.096/32767.0);

    dustLevel = .1-0.17 * sigVolt;

    # Read all the ADC channel values in a list.
    Smoke_val = 0
    CO_val = 0


    # Defining constants
    r0 = 0.38
    ppm = .0

    # The read_adc function will get the value of the specified channel (0-7).
    Smoke_val = adc.read_adc(0, gain=GAIN)*(4.096/32767.0)
    CO_val = adc.read_adc(1, gain=GAIN)

    # Calculating Smoke and CO values
    sensor_volt = CO_val*(4.096/32767.0)
    if sensor_volt == 0:
        RS_gas = 0
    else:
        RS_gas = (4.096 - sensor_volt)/sensor_volt
       
    ratio = RS_gas/r0
    ppm = 47.947*sensor_volt - 79.73501
   

    # Print the ADC values.
    print("Dust Density Level (in ug/m^3): {:.5f}".format(dustLevel));
    print('CO value (Rs\Ro): {:.3f}'.format(ratio))
    print('Smoke value (in V): {:.3f}'.format(Smoke_val))
    print("#########################################")
   
    #if ratio <= 2.0:
    playsound('Soundrec/carbon.wav')
    #if dustLevel >= 10.0:
    playsound('Soundrec/dust.wav')
    #if Smoke_val >= 330:  
    playsound('Soundrec/smoke.wav')
   
   
    # Pause for half a second.
    time.sleep(0.5)

GPIO.cleanup()