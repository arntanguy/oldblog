Title: Install ArchLinux on Dell Latitude E5420 
Date: 2012-03-10 
Tags: linux, archlinux 
Summary: Explains some specific points of Archlinux installation on a Dell Latitude E5420.
disqus_identifier: geenux-install-archlinux-dell-latitude-E5420

Je ne compte pas parler de l’installation d’ArchLinux en lui-même, bien assez de documentation existe sur le sujet.
Je vais me contenter de préciser les parties spécifiques à ce laptop.

# Touchpad

Le touchpad n’est pas un touchpad Synaptics, ce qui complique légèrement la configuration, d’autant plus qu’un bug du noyau fait qu’il n’est pas reconnu en tant que touchpad, mais en temps que souris…
Pour l’installer, il faut installer le paquet AUR
[psmouse-elantech](https://aur.archlinux.org/packages.php?ID=51343), qui compilera un module du noyau linux permettant de corriger le bug.
Voici la démarche à suivre pour le faire :

Ensuite, si vous désirez que le module soit automatiquement compilé quand c’est nécessaire (mise à jour…), mettez le dans le rc.conf

    ::bash
        MODULES="psmouse-elantech"

Ce laptop ne dispose pas de carte graphique, seulement du chipset intégré Intel. Pour le configurer, voici la démarche. Installer le paquet xf86-video-intel

    ::bash
        pacman -S xf86-video-intel

Ensuite, il faut modifier les entrée du grub, si vous désirez disposer de toutes les performances du chipset.
Pour ce faire, éditez le fichier /boot/grub/menu.lst (en root), et modifiez le ainsi

    ::bash
        # (0) Arch Linux
        title Arch Linux
        root (hd0,2)
        kernel /boot/vmlinuz-linux root=/dev/sda3 ro i915.modeset=1
        initrd /boot/initramfs-linux.img

* i915.modeset=1 active le module
* i915.modeset=0 désactive le module
**Attention :** SI vous aviez des entrées vga dans le menu.lst, il faut les enlever !
