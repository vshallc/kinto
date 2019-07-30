#!/usr/bin/env python3
import os, platform, sysconfig, sys, subprocess, time

yellow = "\033[1;33m"
green = "\033[0;32m"
red = "\033[1;31m"
italic = "\033[3m"
reset = "\033[0;0m"

platform_name = platform.system()
# print sysconfig.get_platform()

sys.stdout.write(yellow)
cloud = '\u2601'
circleo = '\u25CE'
clocko = '\u2B6E'
syme = '\u0250'
syma = '\u0251'
# bang = '\u1F589'.decode('unicode-escape')

internalid = 0
usbid = 0

def keyboard_detect():
    global internalid, usbid, chromeswap, system_type
    internal_kbname = ""
    usb_kbname = ""
    print()
    print("Looking for keyboards...")
    print()
    result = subprocess.check_output('xinput list | grep -iv "Virtual\|USB" | grep -i "keyboard.*keyboard" | grep -o -P "(?<=↳).*(?=id\=)";exit 0', shell=True).decode('utf-8')
    if result != "":
        internal_kbname = result.strip()
    internalid = subprocess.check_output('xinput list | grep -iv "Virtual\|USB" | grep -i "keyboard.*keyboard" | cut -d "=" -f 2- | awk \'{print $1}\';exit 0', shell=True).decode('utf-8')
    print("Internal Keyboard\nName: " + internal_kbname + "\nID: " + internalid)

    result = subprocess.check_output('udevadm info -e | grep -o -P "(?<=by-id/usb-).*(?=-event-kbd)" | head -1;exit 0', shell=True).decode('utf-8')
    if result != "":
        usb_kbname = result.strip()

    # Loop the following to ensure the id is picked up after 5-10 tries
    usbid = ""
    usbcount=0
    while usbid == "":
        usbid = subprocess.check_output('udevadm info -e | stdbuf -oL grep -o -P "(?<=event-kbd /dev/input/by-path/pci-0000:00:).*(?=.0-usb)";exit 0', shell=True).decode('utf-8')
        if usbid == "":
            usbcount += 1
            # print('usbid not found '+ str(usbcount))
            if usbcount == 5:
                usbid = "0"
        time.sleep(1)
    print("\nUSB Keyboard\n" + "Name: " + usb_kbname + "\nID: " + usbid)

    if system_type == "1":
        system_type = "windows"
    elif system_type == "2":
        system_type = "chromebook"
    elif system_type == "3":
        system_type = "mac"

    if system_type == "windows" or system_type == "mac":
        cmdgui = '"/usr/bin/setxkbmap -option;/usr/bin/setxkbmap -option altwin:ctrl_alt_win"'
        # subprocess.check_output('echo "1" > /sys/module/hid_apple/parameters/swap_opt_cmd', shell=True).decode('utf-8')
    elif system_type == "chromebook":
        cmdgui = '"setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.gui $DISPLAY"'
        subprocess.check_output('/bin/bash -c ./chromebook.sh', shell=True).decode('utf-8')

    # password = getpass("Please enter your password to complete the keyswap: ")
    # proc = Popen("echo '1' | sudo tee -a /sys/module/hid_apple/parameters/swap_opt_cmd".split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # proc.communicate(password.encode())

    if swap_behavior == 1:
        print("Setting up " + system_type + " keyswap as a service.")
        print("You can disable and remove the service by using the following commands.")
        print("systemctl --user stop keyswap")
        print("systemctl --user disable keyswap")
        print("rm -rf ~/.config/autostart/keyswap.sh")
        print("rm -rf ~/.config/xactive.sh")
        keyswapcmd = '/bin/bash -c "./keyswap_service.sh 1 0 ' + system_type + ' ' + str(internalid).strip() + ' ' + str(usbid) + ' ' + chromeswap '"'
        print(keyswapcmd)
        subprocess.check_output(keyswapcmd, shell=True).decode('utf-8')
    else:
        print("Setting up " + system_type + " keyswap inside your profiles ~/.Xsession file.")
        print("You can modify or remove the file if you want you want to remove the modification.")
        keyswapcmd = '/bin/bash -c "./keyswap_service.sh 0 ' + cmdgui + '"'
        subprocess.check_output(keyswapcmd, shell=True).decode('utf-8')

    print("Please run this command in the terminal if you are using a Windows or Macbook.")
    print("Your keymapping will not work right on Apple keyboards without it.")
    print("echo '1' | sudo tee -a /sys/module/hid_apple/parameters/swap_opt_cmd")
        


def os_detect():
    print()
    print("Checking for OS and system information...")
    print()
    print("OS Type")
    # print(" Platform: " + platform_name)
    if platform_name == 'Linux':
        result = subprocess.check_output("lsb_release -a | grep -v LSB ", shell=True).decode('ascii')
        print(result)

def hwinfo():
    print("Requires user password to display hardware information...")
    result = subprocess.check_output('sudo dmidecode | grep -A 9 "System Information" | grep -v "UUID\|Serial\|SKU\|Wake"', shell=True).decode('ascii')
    print(result)

def kblist():
    result = subprocess.check_output('xinput list', shell=True).decode('ascii')
    print(result)

print()
print()
print("                      K!nt" +  circleo)
sys.stdout.write(reset)
print(italic + "            - F!x the d" + syma + "mn k" + syme + "yb" + circleo + syma + "rd. - ")
sys.stdout.write(reset)
print()
input("Press Enter to begin...")

system_type = input("\nWhat type of system are you using?\n\
    1) Windows\n\
    2) Chromebook\n\
    3) Mac\n")

swap_behavior = 1
chromeswap = 0
# Chromebook
if system_type == "2":
    if not input("\nWould you like to swap Alt to Super/Win and Search key to Ctrl when using terminal applications? (y/n)\n\
Note: For a more mac like experience & less issues with terminal based interactions y is recommended.\n").lower().strip()[:1] == "y":
        swap_behavior = 0
# Windows
if system_type == "1":
    if not input("\nWould you like to swap Alt to Super/Win and Ctrl key back to Ctrl when using terminal applications? (y/n)\n\
Note: For a more mac like experience & less issues with terminal based interactions y is recommended.\n").lower().strip()[:1] == "y":
        swap_behavior = 0
# Mac
if system_type == "3":
    if not input("\nWould you like to swap Command back to Super/Win and Ctrl key back to Ctrl when using terminal applications? (y/n)\n\
Note: For a more mac like experience & less issues with terminal based interactions y is recommended.\n").lower().strip()[:1] == "y":
        swap_behavior = 0

if int(system_type) == 2 and swap_behavior == 1:
    chromeswap = input("\nIf the keyswap is applied on a chromebook with both an internal and external Apple keyboard\n\
you may need to press a key on the external Apple keyboard any time you switch between the terminal and gui based apps.\n\
Are you ok with that, or would you like to only apply the keyswap on one keyboard type?\n\
    1) Built-in\n\
    2) Both - (Chromebook & Windows)\n\
    3) Both - (Chromebook & Mac)\n\
    4) USB External - (Mac)\n")

    if chromeswap == "1":
        chromeswap = "none"
    elif chromeswap == "2":
        chromeswap = "both_win"
    elif chromeswap == "3" or chromeswap == "4":
        chromeswap = "both_mac"

keyboard_detect()