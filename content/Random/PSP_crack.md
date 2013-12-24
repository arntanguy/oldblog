Title: Psp SLIM 200 Chicken & Custom Firmware Gen B 
Date: 2009-12-23 
Tags: psp 
Summary: When using a video card without support for goemetry shaders, ShaderMaker's text editor crashed. Indeed, the code tries to load a geometric shader while this isn't possible. This article provides the necessary source code to fix this issue. 
disqus_identifier: geenux-psp-chicken-firmware

J’ai pas mal galéré pour avoir ma PSP Slim 2000 fonctionnelle avec un custom firmware pour pouvoir lancer des homebrew (applications non officielles), notamment bookr permettant de lire des pdf.

# Installer chickhen r2 

Tout d’abord, qu’est-ce que chickhen ? Il s’agit d’un hack exploitant une faille de la lib tiff de la psp pour permettre le lancement d’homebrew. Une fois chickhen "installé", une bonne partie des homebrews pourront être lancés. Il n’y a aucun risque pour la psp à installer chicken, en effet celui-ci n’est pas réellement installé, la mémoire flash de la psp n’est pas modifié. Chickhen est seulement chargé en mémoire, ce qui signifie que si vous éteignez totalement la psp (en maintenant le bouton off quelques secondes), il faudra le réinstaller, heureusement, cette étape est très simple.

1. Téléchargez [Chickhen](http://geenux.free.fr/downloads/Chickhen.zip)
* Placer le dossier Chickhen dans le dossier PSP/PHOTO
* Placer le fichier h.bin à la racine de votre PSP
* Débrancher la psp, mettez l’adaptateur wlan sur on (ça ne fonctionne pas sinon, en tout cas avec ma psp), assurez vosu que le son n’est pas coupé, puis allez dans le menu Photo->memory stick, et faites croix sur le dossier Chickhen. Là, ne touchez plus à rien, ne scrollez pas, attendez quelques secondes. Il y aura un écran vert qui va apparaître, et la psp va redémarrer. Il se peut que ça ne fonctionne pas si la psp est en français, si c’est le cas, mettez la en anglais (ce que j’ai fait).
* Vérifiez que c’est bien installé, en allant dans le menu Settings->System Information, vous devriez voir 5.03 ChickHEN R2

Là, normalement la plupart des *homebrews* devraient se lancer, mais ça serait dommage de s’arrêter en si bon chemin.


# Installer le custom firmware 5.03 gen B

Il s’agit d’un hack du système d’exploitation de la PSP pour lui ajouter des fonctionnalités et débloquer des choses délibérément bloquées par la psp (pour éviter le piratage des jeux par exemple). Il permettra de lancer les homebrews, les jeux au format iso, cso, boot…

Vous pouvez convertir vos UMD en iso sur votre PSP grâce à ce firmware. Quel intérêt ? Temps de chargement plus rapide, consommation de batterie plus faible, vos UMD ne sont pas abimés.

L’installation est expliquée assez clairement sur
[pspgen](http://www.pspgen.com/custom-firmware-5-03gen-b-for-hen-psp-3000-telechargement-190694.html), je ne vais donc pas le refaire ici.


# Informations complémentaires sur l’utilisation.

Vous pouvez accéder au recovery menu, ainsi qu’au gen vsh menu, permettant de configurer la psp en appuyant sur la touche Select.

Si vous désirez lancer des jeux en iso, il est conseillé de mettre UMS ISO MODE sur Sony NP9960. Si votre iso ne foncitonne pas, essayez M33 driver.

J’espère que ce billet permettra d’éclaircir l’installation du custom firmware. Pour l’installer, j’ai été obligé de faire de nombreuses recherches, sur de nombreux sites/forum, alors que c’est extrêmement simple et sur (j’avais peur de bricker ma psp, et il m’a fallu voir plusieurs sites pour être convaincu que le flash0 n’était pas touché).
