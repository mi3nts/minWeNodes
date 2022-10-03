
import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()

debug  = False 

def main():
    while True:
        try:
            batteryLevelRaw = wpi.analogRead(25)
            time.sleep(30)
        
            batteryLevel    = batteryLevelRaw*(2.1*2)/(4095)
            batteryLevelPer = batteryLevel*(100/4.2)
            referenceLev    = wpi.analogRead(29)
            print("======= Battery Readings =======")
            print("Reference Level:          " + str(referenceLev))
            print("---------------------------------")
            print("Battery Level Raw:        " + str(batteryLevelRaw))
            print("---------------------------------")
            print("Battery Level:            " + str(batteryLevel)+" V")
            print("---------------------------------")
            print("Battery Level Percentage: " + str(batteryLevelPer)+" %")    

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    print("Monitoring Battery level for Mints Wearable Node")
    