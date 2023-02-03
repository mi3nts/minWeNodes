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
```
ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 00:1e:06:4a:15:1d brd ff:ff:ff:ff:ff:ff
    inet 10.11.1.14/24 brd 10.11.1.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::21e:6ff:fe4a:151d/64 scope link 
       valid_lft forever preferred_lft forever
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 2312 qdisc mq state UP group default qlen 1000
    link/ether e8:4e:06:95:5e:38 brd ff:ff:ff:ff:ff:ff
    inet 192.168.31.237/24 brd 192.168.31.255 scope global dynamic noprefixroute wlan0
       valid_lft 84927sec preferred_lft 84927sec
    inet6 fe80::440d:85e6:8f7:a279/64 scope link dadfailed tentative noprefixroute 
       valid_lft forever preferred_lft forever
    inet6 fe80::1708:79a0:3d3b:b4cf/64 scope link dadfailed tentative noprefixroute 
       valid_lft forever preferred_lft forever
    inet6 fe80::9755:f3f7:3198:eaa8/64 scope link dadfailed tentative noprefixroute 
       valid_lft forever preferred_lft forever
 ```
 - Configure the static IP 
``` sudo nano /etc/network/interfaces ```
```
# ifupdown has been replaced by netplan(5) on this system.  See
# /etc/netplan for current configuration.
# To re-enable ifupdown on this system, you can run:
#    sudo apt install ifupdown
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
  address 10.11.1.18
  netmask 255.255.255.0
```
- Restart network
```
teamlary@odroid:~$ sudo /etc/init.d/networking restart
Restarting networking (via systemctl): networking.service.
```
- For this to work when rebooting do the following 
```
sudo nano /etc/network/interfaces
```
```
# ifupdown has been replaced by netplan(5) on this system.  See
# /etc/netplan for current configuration.
# To re-enable ifupdown on this system, you can run:
#    sudo apt install ifupdown
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet static
  address 10.11.1.18
  netmask 255.255.255.0
```

