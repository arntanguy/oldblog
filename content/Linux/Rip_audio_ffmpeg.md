Title: Ripper l'audio d'une vidéo avec FFMPEG.
Date: 2011-12-19 
Tags: linux, ffmpeg, audio, video, rip 
Summary: Ripping audio from videos using ffmpeg 
disqus_identifier: geenux-ripper-audio-video-ffmpeg

Bonjour,
Vu que j’ai eu un peu de mal à trouver comment ripper la bande son d’une vidéo (en l’occurence de youtube), j’ai fait un petit script pour le faire simplement :

    ::bash
        #!/bin/bash
 
        ### libmp3lame required : to install
        #sudo apt-get install ffmpeg libavcodec-extra-52
         
        for i in "$*"; do
        #mplayer -ao pcm "$i" -ao pcm:file="$(echo "$i"|cut -d'.' -f1).mp3"
        # -vn remove the video
        ffmpeg -i "$i" -vn -acodec libmp3lame "$(echo "$i"|cut -d'.' -f1).mp3"
        done

Très simple à utiliser, faites juste

    ::bash
        ripaudio.sh fichier1.flv fichier2.mpeg ...
