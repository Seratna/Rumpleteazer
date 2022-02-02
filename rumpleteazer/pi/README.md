# Raspberry Pi

## Raspberry Pi OS
[Install Raspberry Pi OS using Raspberry Pi Imager](https://www.raspberrypi.com/software/)

or use
```bash
sudo apt install rpi-imager
```

## enable SSH
Create an empty file with the name `ssh` and put it on the `boot` partition.
```bash
cd /media/antares/boot
touch ssh
```

## enable WiFi
### get a hash of the password
```commandline
wpa_passphrase YOUR_WIFI_NAME YOUR_PASSWORD
```
### add config file
define a `wpa_supplicant.conf` file for your particular wireless network.
Put this file onto the `boot` folder of the SD card.
```text
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=CN
update_config=1

network={
  ssid=<ssid>
  psk=<hash>
}

```

## enable HID
1.  ssh into the pi
2.  install dependencies
    ```bash
    sudo apt-get update
    sudo apt-get install git vim python3-pip xxd
    ```

3.  enable the necessary modules and drivers
    ```bash
    sudo echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
    sudo echo "dwc2" | sudo tee -a /etc/modules
    sudo echo "libcomposite" | sudo tee -a /etc/modules
    ```

4.  setup

    1.  create a new setup file
        ```bash
        sudo vim /usr/bin/hid_setup.py
        ```
        then copy the code in `hid_setup.py` into this new file and save.

    2.  config to run this script automatically at startup
        ```bash
        sudo vim /etc/rc.local
        ```
        then add `python3 /usr/bin/hid_setup.py` before `exit 0`

    3.  reboot
        ```bash
        sudo reboot
        ```

## references
https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition/
https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-report-descriptor/
https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-send-reports/
