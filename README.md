# minWeNodes
Contains firmware for Mints Wearable Nodes

## Battery Voltage Reader Circuit 

- Larger Resister 560 K 
- Smaller Resister 180 K 

Inspired from https://blog.voltaicsystems.com/reading-charge-level-of-voltaic-usb-battery-packs/

ADC: https://wiki.odroid.com/common/application_note/gpio/wiringpi

## Setting up the IP Address
- Check IP 
```
teamlary@odroid:~$ ifconfig
eth0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 10.11.1.14  netmask 255.255.255.0  broadcast 10.11.1.255
        inet6 fe80::21e:6ff:fe4a:151d  prefixlen 64  scopeid 0x20<link>
        ether 00:1e:06:4a:15:1d  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 270  bytes 55405 (55.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 21  
       
```
