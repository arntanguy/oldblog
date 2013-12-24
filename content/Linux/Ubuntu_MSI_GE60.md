Title: Install Ubuntu on MSI-GE60 0NC 
Date: 2013-05-10 
Tags: linux, ubuntu 
Summary: Just some pointers on installing Ubuntu on a MSI-GE60 ONC
disqus_identifier: geenux-install-ubuntu-msi-ge60

Hi,
It’s been a while since I last had a bit of trouble installing Ubuntu, so I decided to write a small article about it.
Don’t expect screenshots, I don’t want to go back to the installer just for the sake of some nice images.

I will here explain how I installed a dualboot Windows 8/Ubuntu on my new **MSI GE60 ONC** laptop.

# UEFI

The main difference I encountered was the introduction of UEFI. Don’t worry if you had never heard of that before, I discovered it while installing Ubuntu on my new laptop as well! Basically, it is meant to replace the old BIOS architecture with a more flexible one.

What the [Ubuntu documentation](https://help.ubuntu.com/community/UEFI) on UEFI recommends is to install both Windows and Ubuntu using the UEFI mode.

Unfortunately, for some reason that I was unable to figure out, I wasn’t able to properly boot the LiveUSB on UEFI mode: it kept on giving me a black screen (and from what I saw on the forums, I’m not the only one).

![UEFI]({filename}/images/linux/UEFI.jpg)

The workaround I used consists of booting and installing in Legacy Mode. To go into legacy mode, just press "Del." on startup to enter the BIOS, and change the "Boot" options to Legacy instead of UEFI.

Then, install the dualboot as usual (reduce windows partition size, create a new one for linux, extend the Data partition, add a swap partition).

You will also need to create a special partition for the BIOS support of Legacy. To do so, create a small partition using gparted (>1Mb), and set the Flag grub_bios (or something like that).

You’re done.

Now,

* to start Linux, go into the BIOS and set it to Legacy
* to start Windows, go into the BIOS and set it to UEFI

I know, it’s quite an ugly workaround, but that did the trick, and I’m barely even starting windows, so for me going into the bios when I need to start it is not so much of a bother.

You could try using the boot-repair utility to convert the legacy booting process to UEFI. It is supposed to work quite well, however I ran into topics of users that tried it and failed. So I didn’t bother investigating any further. Let me know if you manage to do it successfully ;)
