Title: Script de téléchargement pour mangareader.net 
Date: 2012-02-05 
Tags: programmation, python, manga, script 
Summary: Reading mangas online is a pain, so why not download them? That's what this script is for, use it wisely!
disqus_identifier: geenux-script-download-mangareader


J’ai réalisé un petit script python pour télécharger les mangas depuis le site
<http://mangareader.net>.
Ce script fonctionne pour tous les mangas que j’ai testé, je suppose qu’il fonctionne pour le reste.
Le code est un peu sale, gestion des exceptions pas très rigoureuse (si il y a une erreur durant le téléchargement, pas de souci, vous serez prévenu), appel de fonctions qui pourraient être évités…
Si je suis pas trop flemmard, je modifierai ça plus tard.

Il n’est probablement pas légal d’utiliser ce script sans être en possession des mangas originaux, pensez à les acheter !

Le script est sous licence GNU GPL, vous êtes libres de le modifier, l’utiliser comme bon vous semble. Si vous l’améliorez, j’apprécierai d’avoir le nouveau script.

Utilisation
Tout d’abord, il faut modifier quelques paramètres dans le script pour l’adapter à vos besoin.
La variable DL_DIR contient le répertoire dans lequel vous souhaitez stocker les mangas, adaptez la à vos besoin.

Pour utiliser le script, il suffit de faire

    ::bash
        mangareader.py "one piece" 199

Cette commande télécharge le chapitre 199 de One Piece.

    ::bash
        mangareader.py "fairy tail" 1-112

Cette commande télécharge les chapitres de 1 à 112 de Fairy Tail

Voici donc le script en question:

    ::python
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        """A small script that downloads mangas from onemanga.com
            Licenced under the WTPL Licence"""

        import os
        import re
        import socket
        import sys
        import urllib

        def helper():
            """Gives help about the use of this script"""
            print """Usage:
                - python """+sys.argv[0]+""" manga chapter
                - python """+sys.argv[0]+""" manga firstchap-lastchap
                """
            exit(0)

        # Config
        MAXTRIES = 5
        DL_DIR = "/media/DATA/Mangas/"
        MANGA_LIST = "http://www.mangareader.net/alphabetical"
        MANGA_SITE = "http://www.mangareader.net"
        CHAPTER_NUMBER_LENGTH=3

        def print_error(text):
            print "\033[31;1m" + text + "\033[0m"

        def print_sucess(text):
            print "\033[32;40m"+text+"\033[0m"

        def down(url):
            """Download the webpage at the given url"""
            tries = 0
            downloaded = False
            while tries < MAXTRIES and downloaded == False:
                try:
                    ret = urllib.urlopen(url)
                    downloaded = True
                except (IOError, socket.error):
                    tries += 1
                    print_error("Failed download, retrying...")
            if tries == MAXTRIES:
                print_error("Maximum tries number reached exiting...")
                exit(1)
            if tries==0:
                print_sucess("Downloaded !")

            return ret

        def retrieve(url, nom):
            """Retrieves a file"""
            tries = 0
            downloaded = False
            while tries < MAXTRIES and downloaded == False:
                try:
                    urllib.urlretrieve(url, nom)
                    downloaded = True
                except (socket.error, IOError):
                    tries += 1
                    if tries == MAXTRIES:
                        print_error("Maximum tries number reached exiting...")
                        exit(1)
                    else:
                        print_error("Failed download, retrying...")
                if tries==0:
                    print_sucess(nom+" downloaded.")

        def make_pretty(name):
            """Returns the chain given, in order to have a normal name"""
            return str(name).capitalize().replace("/", "").replace("_", " ")

        class Mangareader:
            """Manga class.
            Contains several attributes related to the manga.
            Contains also methods to download its chapters"""

            def __init__(self,manga):
                self.manga = manga
                self.manga_p = make_pretty(manga)
                self.url = "http://mangareader.net/"
                self.nb_image=0
                # Create the download directory
                try:
                    if (os.path.isdir(DL_DIR) == False):
                        os.mkdir(DL_DIR)
                    if (os.path.isdir(DL_DIR + self.manga_p) == False):
                        os.mkdir(DL_DIR + self.manga_p)
                except OSError:
                    print_error("Unable to create the download directory")
                    exit(1)

            def chap_dir_name(self, number):
                """Returns the name of the directory of the chapter.
                    It is useful in order to organize the mass of chapters.
                    example:
                    500 chaps in the manga, directory named "001" instead of "1" """
                num = str(number)
                return (CHAPTER_NUMBER_LENGTH - len(num))*"0"+ num


            def get_chapter(self, number):
                """ Get the images page url list """
                print "Downloading chapter "+self.chap_dir_name(number)
                url = MANGA_SITE+ "/" + self.manga + "/" + str(number)
                page = down(url).read()
                #print page
                exp = 'select> of ([0-9]+).*<'
                try:
                    self.nb_images = int(re.search(exp, page).group(1))
                    #print nb_images
                except:
                    print_error("Cannot determine the number of images in this chapter")
                #<option value="/103-2057-1/one-piece/chapter-12.html" selected="selected">1</option>
                exp = '<option value="(.*)">(.+)</option>'
                exp2 = '<option value="(.*)" selected="selected">(.+)</option>'

                # get the link for all pages containing chapter images
                img = re.findall(exp, page)
                images=[]

                try:
                    images.append(re.findall(exp2, page)[0][0])
                except:
                    print_error( "Une page n'a pas été trouvée !")

                # remove the problem with the special case of the current image
                for l in img:
                    el=l[0]
                    if(el.find("selected") < 0):
                        images.append(el)

                manga_dir = DL_DIR + self.manga_p +"/" + self.chap_dir_name(number)
                try:
                    if (os.path.isdir(manga_dir) == False):
                        os.mkdir(manga_dir)
                except OSError:
                    print_error("Unable to create the download directory")
                    exit(1)
                os.chdir(manga_dir)

                self.get_images(images)

            def get_images(self,images_url):
                 #<img id="img" width="800" height="1210" src="http://i28.mangareader.net/one-piece/133/one-piece-1690829.jpg" alt="One Piece 133 - Page 15" name="img" />
                exp = '<img id=.* width=.* height=.* src="(.*)" alt=.* name=.* />'
                images = []
                for url in images_url:
                    print "Parsing page "+url
                    page = down(MANGA_SITE+url).read()
                    img = re.findall(exp,page)
                    try:
                        images.append(img[0])
                    except:
                        print_error("Un lien vers une image n'a pas été correctement récupéré!")

                i=1
                for img in images:
                    if len(images) == self.nb_images:
                        print "Téléchargement de l'image "+str(i)+"/"+str(self.nb_images)
                        retrieve(img, self.manga_p+"-"+self.chap_dir_name(i))
                        i+=1
                    else:
                        print_error("Le nombre d'images à télécharger est différent du nombre d'images du chapitre ! Tout ne sera pas téléchargé !")



        if len(sys.argv) != 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            helper()
            exit(0)
        elif len(sys.argv) == 1:
            helper()
            exit(0)

        if ((len(sys.argv) == 2) and (sys.argv[1]=="Is there an easter egg in this awesome program ?")):
            print "     __/~~\-''- _ |     "
            print "__- - {            \    "
            print "     /             \    "
            print "    /       ;o    o }   "
            print "    |              ;    "
            print "                   '    "
            print "       \_       (..)    "
            print "         ''-_ _ _ /     "
            print "           /            "
            print "          /             "



        if len(sys.argv) == 3:
            M = Mangareader(sys.argv[1])
            chap = sys.argv[2]
            if chap.find("-") > 0:
                chap = chap.split("-")
                if(len(chap) == 2):
                    for i in range(int(chap[0]),int(chap[1])):
                        M.get_chapter(i)
            else:
                M.get_chapter(sys.argv[2])
