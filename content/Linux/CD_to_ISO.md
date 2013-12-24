Title: Useful usages of dd.
Date: 2011-08-13 
Tags: linux, ISO, CD, bash 
Summary: Why use a graphical application to convert a CD to ISO when you can use dd? Or to create a bootable USB stick? In this post you'll see some very useful usages of the **dd** command.
disqus_identifier: geenux-useful-usage-of-dd 

Hello world,
Why bother using heavy and complicated tools to create and use ISO files? Why
not simply consider using the **dd** command?
Granted, this command can sometimes look quite scary, especially because of
it's impressive potential to destroy data with a misintruction.
Still, it's a very useful command, just be careful how you use it!

# Create an ISO image of a CD

Data within a CD are commonly wrapped in an ISO-9660 filesystem. An ISO image
is merely a copy of this filesystem in a single file.
Seen like that, the solution spawns naturally: we merely neeed to do a bit by
bit copy of the CD into a file...
Who said **dd** is meant for that?
Just run

    ::bash
        dd if=/dev/cdrom of=cd.iso

# Mount ISO 
Mountin an ISO can always be useful, so here is how to do it.

    ::bash
        sudo mkdir /mnt/iso
        sudo mount -t iso9660 -o loop cd.iso /mnt/iso
        ls /mnt/iso



# Create bootable USB key
Assuming you USB key is on */dev/sdb*, and **isn't mounted**, you can simply
run the following command to create a bootable USB key.
Note that it is sd**b** and not sd**b1**. Indeed, we do want to copy the
bootloader and the partition table as well.

    ::bash
        dd bs=4M if=bootable_iso.iso of=/dev/sdb

