Title: Configure USB debugging of Android on GNU/Linux 
Date: 2012-02-05 
Tags: programmation, android, linux 
Summary: When using a video card without support for goemetry shaders,
ShaderMaker's text editor crashed. Indeed, the code tries to load a geometric
shader while this isn't possible. This article provides the necessary source
code to fix this issue. 
disqus_identifier: geenux-usb-debugging-android


You want to develop your own application and test it directly your phone instead of the virtual machine? Or perhaps you just want to use some cool features of the SDK to manage your phone? Whatever the reason, here is how to do it.

First, I’ll assume that you have already installed the android SDK.

The only thing left to do, is to set-up rules for udev. Most articles are happy with giving you a list of devices and Vendor ID. Well, I’m not. These lists are often not exhaustive, and unusual android devices are not represented. There is a really simple way of figuring out this data.
Simply use the command

    ::bash
        lsusb
 
It will give you a description of all your USB devices, find the one
corresponding to your device

    ::bash
        Bus 002 Device 004: ID 04e8:689e Samsung Electronics Co., Ltd 

All the information you need is in this line : the vendor ID is 04e8, and the device id is 689e (this is a Samsung Galaxy Ace).

You just have to declare it to udev:

    ::bash
        sudo vim /etc/udev/rules.d/51-android.rules

Then put a line like:

    ::bash
        SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", , ATTRS{idProduct}=="689e", MODE="0666"

Obviously you need to set your own vendor and device ID here.

You’re all set! Next time udev will restart, your device should work!
